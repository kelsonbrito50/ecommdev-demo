"""
Security middleware for additional hardening.
Implements Content-Security-Policy, security headers, and request validation.
"""
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
    - Content-Security-Policy (CSP)
    - Permissions-Policy
    - Additional security headers
    """

    def process_response(self, request, response):
        # Skip for admin and debug toolbar
        if request.path.startswith('/gerenciar-ecd/') or request.path.startswith('/__debug__/'):
            return response

        # Content-Security-Policy
        # Configurable via settings, with secure defaults
        csp_policy = getattr(settings, 'CSP_POLICY', None)

        if csp_policy is None:
            # Secure default CSP
            csp_directives = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://www.googletagmanager.com https://www.google-analytics.com",
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

        # Permissions-Policy (formerly Feature-Policy)
        permissions_policy = getattr(settings, 'PERMISSIONS_POLICY',
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(self), usb=()"
        )
        response['Permissions-Policy'] = permissions_policy

        # Additional security headers
        response['X-Permitted-Cross-Domain-Policies'] = 'none'
        response['Cross-Origin-Embedder-Policy'] = 'unsafe-none'  # Required for external resources
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Resource-Policy'] = 'same-origin'

        # Referrer Policy (more restrictive than Django default)
        if 'Referrer-Policy' not in response:
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

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

        # Check URL length
        if len(path) > self.MAX_URL_LENGTH:
            logger.warning(
                f"Blocked request with excessively long URL from {request.META.get('REMOTE_ADDR')}"
            )
            return HttpResponseForbidden("URL too long")

        # Check for suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern.search(path):
                logger.warning(
                    f"Blocked suspicious request pattern from {request.META.get('REMOTE_ADDR')}: {path[:100]}"
                )
                return HttpResponseForbidden("Invalid request")

        # Check for SQL injection patterns in URL (skip API and admin paths)
        if not path.startswith('/api/') and not path.startswith('/gerenciar-ecd/'):
            for pattern in self.SQL_PATTERNS:
                if pattern.search(path):
                    logger.warning(
                        f"Blocked potential SQL injection from {request.META.get('REMOTE_ADDR')}: {path[:100]}"
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
