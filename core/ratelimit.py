"""
Simple rate limiting for authentication endpoints.
Uses Django's built-in cache framework - no external dependencies.
"""

from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

# Trusted proxy IPs - only trust X-Forwarded-For from these IPs
# Configure this in settings.py: TRUSTED_PROXY_IPS = ['10.0.0.1', '10.0.0.2']
TRUSTED_PROXY_IPS = getattr(settings, "TRUSTED_PROXY_IPS", [])

# Number of trusted proxies in the chain (for multiple proxies)
# If you have: Client -> Cloudflare -> Nginx -> App, set to 2
NUM_TRUSTED_PROXIES = getattr(settings, "NUM_TRUSTED_PROXIES", 1)


def get_client_ip(request):
    """
    Get client IP address from request securely.

    SECURITY: Only trusts X-Forwarded-For header when the direct connection
    comes from a known trusted proxy. This prevents IP spoofing attacks
    that could bypass rate limiting.
    """
    remote_addr = request.META.get("REMOTE_ADDR", "")

    # Only trust X-Forwarded-For if request comes from a trusted proxy
    if TRUSTED_PROXY_IPS and remote_addr in TRUSTED_PROXY_IPS:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # X-Forwarded-For format: client, proxy1, proxy2, ...
            # The rightmost untrusted IP is the client IP
            ips = [ip.strip() for ip in x_forwarded_for.split(",")]

            # If we have multiple trusted proxies, skip them from the right
            # to get the actual client IP
            if len(ips) > NUM_TRUSTED_PROXIES:
                # Get the IP just before the trusted proxy chain
                client_ip = ips[-(NUM_TRUSTED_PROXIES + 1)]
            else:
                # Fall back to first IP if chain is shorter than expected
                client_ip = ips[0]

            return client_ip

    # Default: use the direct connection IP (REMOTE_ADDR)
    # This is the safest option when not behind a trusted proxy
    return remote_addr


class RateLimiter:
    """
    Simple rate limiter using Django's cache.

    Usage:
        @RateLimiter(key='login', rate='5/m')
        def login_view(request):
            ...

    Rate formats:
        - '5/m' = 5 requests per minute
        - '100/h' = 100 requests per hour
        - '1000/d' = 1000 requests per day
    """

    def __init__(self, key="default", rate="10/m", block_time=300):
        """
        Initialize rate limiter.

        Args:
            key: Unique key for this rate limit (e.g., 'login', 'register')
            rate: Rate limit in format 'count/period' (m=minute, h=hour, d=day)
            block_time: How long to block after limit exceeded (seconds)
        """
        self.key = key
        self.block_time = block_time
        self.limit, self.period = self._parse_rate(rate)

    def _parse_rate(self, rate):
        """Parse rate string like '5/m' into (count, seconds)."""
        count, period = rate.split("/")
        count = int(count)

        period_map = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
        }
        seconds = period_map.get(period, 60)
        return count, seconds

    def _get_cache_key(self, request):
        """Generate cache key based on IP and rate limit key."""
        ip = get_client_ip(request)
        return f"ratelimit:{self.key}:{ip}"

    def _get_block_key(self, request):
        """Generate block key for temporarily blocked IPs."""
        ip = get_client_ip(request)
        return f"ratelimit:blocked:{self.key}:{ip}"

    def is_blocked(self, request):
        """Check if this IP is currently blocked."""
        block_key = self._get_block_key(request)
        return cache.get(block_key) is not None

    def check_rate_limit(self, request):
        """
        Check if request is within rate limit.

        Returns:
            tuple: (allowed: bool, remaining: int, reset_time: int)
        """
        # Check if blocked
        if self.is_blocked(request):
            return False, 0, self.block_time

        cache_key = self._get_cache_key(request)

        # Get current count
        current = cache.get(cache_key, {"count": 0, "reset": 0})

        import time

        now = time.time()

        # Check if period has reset
        if now > current.get("reset", 0):
            current = {"count": 0, "reset": now + self.period}

        # Check if over limit
        if current["count"] >= self.limit:
            # Block this IP
            block_key = self._get_block_key(request)
            cache.set(block_key, True, self.block_time)
            return False, 0, self.block_time

        # Increment count
        current["count"] += 1
        cache.set(cache_key, current, self.period)

        remaining = self.limit - current["count"]
        return True, remaining, int(current["reset"] - now)

    def __call__(self, view_func):
        """Decorator for views."""

        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            allowed, remaining, reset = self.check_rate_limit(request)

            if not allowed:
                return HttpResponseForbidden(
                    _("Muitas tentativas. Por favor, aguarde %(minutes)d minutos.")
                    % {"minutes": reset // 60 or 1}
                )

            response = view_func(request, *args, **kwargs)

            # Add rate limit headers
            response["X-RateLimit-Limit"] = str(self.limit)
            response["X-RateLimit-Remaining"] = str(remaining)
            response["X-RateLimit-Reset"] = str(reset)

            return response

        return wrapped_view


class RateLimitMixin:
    """
    Mixin for class-based views to add rate limiting.

    Usage:
        class LoginView(RateLimitMixin, View):
            ratelimit_key = 'login'
            ratelimit_rate = '5/m'
            ratelimit_block = 300
    """

    ratelimit_key = "default"
    ratelimit_rate = "10/m"
    ratelimit_block = 300

    def dispatch(self, request, *args, **kwargs):
        limiter = RateLimiter(
            key=self.ratelimit_key, rate=self.ratelimit_rate, block_time=self.ratelimit_block
        )

        allowed, remaining, reset = limiter.check_rate_limit(request)

        if not allowed:
            return HttpResponseForbidden(
                _("Muitas tentativas. Por favor, aguarde %(minutes)d minutos.")
                % {"minutes": reset // 60 or 1}
            )

        response = super().dispatch(request, *args, **kwargs)

        # Add rate limit headers
        response["X-RateLimit-Limit"] = str(limiter.limit)
        response["X-RateLimit-Remaining"] = str(remaining)
        response["X-RateLimit-Reset"] = str(reset)

        return response


# Convenience instances for common use cases
login_ratelimit = RateLimiter(key="login", rate="5/m", block_time=300)
register_ratelimit = RateLimiter(key="register", rate="3/m", block_time=600)
password_reset_ratelimit = RateLimiter(key="password_reset", rate="3/m", block_time=600)
api_ratelimit = RateLimiter(key="api", rate="60/m", block_time=60)
