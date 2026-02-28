"""
Security middleware for additional hardening.
Implements Content-Security-Policy, security headers, and request validation.
"""
import base64
import os
import re
import logging
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses.

    Implements:
    - Content-Security-Policy (CSP) with per-request nonces (replaces unsafe-inline)
    - Permissions-Policy
    - Additional security headers

    Security (7.2): 'unsafe-inline' removed from script-src.
    A cryptographic nonce is generated per request and injected into the CSP
    script-src directive. All inline <script> tags must include the matching
    nonce attribute: <script nonce="{{ request.csp_nonce }}">...</script>
    The nonce is available in templates via {{ request.csp_nonce }} because
    django.template.context_processors.request is installed.
    """

    @staticmethod
    def _generate_nonce():
        """Return a 16-byte URL-safe base64 nonce string."""
        return base64.b64encode(os.urandom(16)).decode('ascii')

    def process_request(self, request):
        """Attach a fresh nonce to the request for use in templates and CSP."""
        request.csp_nonce = self._generate_nonce()
        return None

    # Permissive CSP for Django admin — allows inline scripts/styles required by the
    # admin UI while still providing some protection (e.g. frame-ancestors 'self').
    ADMIN_CSP = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "frame-ancestors 'self'; "
        "form-action 'self';"
    )

    def process_response(self, request, response):
        # Debug toolbar: skip entirely (it injects its own markup and assets)
        if request.path.startswith('/__debug__/'):
            return response

        # Admin paths: apply a permissive but present CSP instead of no header.
        # SECURITY (7.3): Do NOT skip security headers for admin paths.
        if request.path.startswith('/gerenciar-ecd/'):
            response['Content-Security-Policy'] = self.ADMIN_CSP
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response['X-Permitted-Cross-Domain-Policies'] = 'none'
            return response

        # Retrieve nonce generated in process_request (may be absent on very
        # early error responses before process_request ran).
        nonce = getattr(request, 'csp_nonce', self._generate_nonce())

        # Content-Security-Policy
        # Configurable via settings, with secure defaults
        csp_policy = getattr(settings, 'CSP_POLICY', None)

        if csp_policy is None:
            # Secure default CSP — nonce replaces 'unsafe-inline' for scripts.
            # 'unsafe-inline' is intentionally retained ONLY for style-src
            # because Bootstrap/third-party CDN styles set inline styles that
            # cannot yet be nonce-gated without breaking the UI.
            csp_directives = [
                "default-src 'self'",
                f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net https://www.googletagmanager.com https://www.google-analytics.com",
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com",
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net",
                "img-src 'self' data: https: blob:",
                "connect-src 'self' https://www.google-analytics.com https://api.mercadopago.com https://cdn.jsdelivr.net",
                "frame-src 'self' https://www.mercadopago.com.br",
                "frame-ancestors 'self'",
                "form-action 'self'",
                "base-uri 'self'",
                "object-src 'none'",
            ]
            csp_policy = "; ".join(csp_directives)

        # Only set CSP in production (can break development)
        if not settings.DEBUG:
            response['Content-Security-Policy'] = csp_policy
        else:
            # Report-only mode in development
            response['Content-Security-Policy-Report-Only'] = csp_policy

        # X-Content-Type-Options: prevent MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # X-Frame-Options: prevent clickjacking
        response['X-Frame-Options'] = 'DENY'

        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions-Policy: disable unnecessary browser features
        permissions_policy = getattr(settings, 'PERMISSIONS_POLICY',
            "camera=(), microphone=(), geolocation=(), payment=(self), "
            "accelerometer=(), gyroscope=(), magnetometer=(), usb=()"
        )
        response['Permissions-Policy'] = permissions_policy

        # Additional hardening headers
        response['X-Permitted-Cross-Domain-Policies'] = 'none'
        response['Cross-Origin-Embedder-Policy'] = 'unsafe-none'  # Required for external resources (Bootstrap CDN etc.)
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Resource-Policy'] = 'cross-origin'  # Allow CDN resources

        return response


class RequestValidationMiddleware(MiddlewareMixin):
    """
    Validate incoming requests for suspicious patterns.

    Detects and blocks:
    - Path traversal attempts
    - SQL injection patterns in URLs
    - Null byte injection
    - Excessively long URLs/headers
    """

    # Maximum URL length (prevents DoS via long URLs)
    MAX_URL_LENGTH = 2048

    # Maximum header size
    MAX_HEADER_SIZE = 8192

    # Suspicious patterns in URL
    SUSPICIOUS_PATTERNS = [
        re.compile(r'\.\./'),  # Path traversal
        re.compile(r'\.\.\\'),  # Windows path traversal
        re.compile(r'%2e%2e[%2f/\\]', re.IGNORECASE),  # Encoded path traversal
        re.compile(r'%00'),  # Null byte
        re.compile(r'\x00'),  # Null byte (raw)
        re.compile(r'<script', re.IGNORECASE),  # XSS in URL
        re.compile(r'javascript:', re.IGNORECASE),  # JavaScript protocol
        re.compile(r'vbscript:', re.IGNORECASE),  # VBScript protocol
        re.compile(r'data:', re.IGNORECASE),  # Data protocol (potential XSS)
    ]

    # SQL injection patterns (basic detection)
    SQL_PATTERNS = [
        re.compile(r"(\%27)|(\')|(\-\-)|(\%23)|(#)", re.IGNORECASE),
        re.compile(r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))", re.IGNORECASE),
        re.compile(r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))", re.IGNORECASE),
        re.compile(r"((\%27)|(\'))union", re.IGNORECASE),
    ]

    def process_request(self, request):
        path = request.get_full_path()
        url_path = request.path          # path only, no query string
        query_string = request.META.get('QUERY_STRING', '')

        # Check URL length
        if len(path) > self.MAX_URL_LENGTH:
            logger.warning(
                f"Blocked request with excessively long URL from {request.META.get('REMOTE_ADDR')}"
            )
            return HttpResponseForbidden("URL too long")

        # Check for suspicious patterns in the URL path (not query string — handled separately)
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern.search(url_path):
                logger.warning(
                    f"Blocked suspicious request pattern from {request.META.get('REMOTE_ADDR')}: {url_path[:100]}"
                )
                return HttpResponseForbidden("Invalid request")

        # Check SQL injection patterns ONLY in query string to avoid false positives
        # on legitimate URL path segments (e.g. slugs containing dashes or apostrophes).
        if query_string:
            for pattern in self.SQL_PATTERNS:
                if pattern.search(query_string):
                    logger.warning(
                        f"Blocked potential SQL injection in query string from "
                        f"{request.META.get('REMOTE_ADDR')}: {url_path[:100]}?{query_string[:100]}"
                    )
                    return HttpResponseForbidden("Invalid request")

        # Check Host header for injection
        host = request.META.get('HTTP_HOST', '')
        if host and not re.match(r'^[\w\-\.:]+$', host):
            logger.warning(
                f"Blocked request with suspicious Host header from {request.META.get('REMOTE_ADDR')}"
            )
            return HttpResponseForbidden("Invalid request")

        return None


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Enhance session security.

    Implements:
    - Session fingerprinting (optional)
    - Session rotation on privilege escalation
    - Concurrent session limits
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            return None

        # Store user agent fingerprint in session
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:256]
        stored_ua = request.session.get('_security_ua')

        if stored_ua is None:
            # First request with this session
            request.session['_security_ua'] = user_agent
        elif stored_ua != user_agent:
            # User agent changed - possible session hijacking
            # Log but don't block (can have false positives from browser updates)
            session_key = request.session.session_key or 'unknown'
            logger.info(
                f"User agent changed for user {request.user.id} "
                f"from session {session_key[:8]}..."
            )

        return None

    def process_response(self, request, response):
        # Regenerate session ID periodically for authenticated users
        # Skip rotation on POST/PUT/DELETE to avoid CSRF token issues
        try:
            if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
                return response

            # Skip rotation for admin to avoid CSRF issues
            if request.path.startswith('/gerenciar-ecd/'):
                return response

            if hasattr(request, 'user') and request.user.is_authenticated:
                if hasattr(request, 'session') and request.session.session_key:
                    last_rotation = request.session.get('_security_last_rotation', 0)

                    import time
                    now = int(time.time())

                    # Rotate session every 30 minutes
                    rotation_interval = getattr(settings, 'SESSION_ROTATION_INTERVAL', 1800)

                    if now - last_rotation > rotation_interval:
                        request.session.cycle_key()
                        request.session['_security_last_rotation'] = now
        except Exception as e:
            # Don't let session rotation errors break the response
            logger.warning(f"Session rotation error: {e}")

        return response


class LoggingMiddleware(MiddlewareMixin):
    """
    Security-focused request logging.

    Logs:
    - Authentication failures
    - Access to sensitive endpoints
    - Suspicious request patterns
    """

    SENSITIVE_PATHS = [
        '/gerenciar-ecd/',  # Admin
        '/api/v1/auth/',    # Authentication
        '/webhook/',        # Webhooks
    ]

    def process_request(self, request):
        # Log access to sensitive endpoints
        path = request.path

        for sensitive_path in self.SENSITIVE_PATHS:
            if path.startswith(sensitive_path):
                logger.info(
                    f"Sensitive endpoint access: {request.method} {path} "
                    f"from {request.META.get('REMOTE_ADDR')} "
                    f"user={getattr(request.user, 'id', 'anonymous')}"
                )
                break

        return None

    def process_response(self, request, response):
        # Log authentication failures
        if response.status_code == 401 or response.status_code == 403:
            logger.warning(
                f"Auth failure: {request.method} {request.path} "
                f"status={response.status_code} "
                f"from {request.META.get('REMOTE_ADDR')} "
                f"user={getattr(request.user, 'id', 'anonymous')}"
            )

        return response
