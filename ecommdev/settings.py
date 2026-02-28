"""
Django settings for ECOMMDEV - Web Development Agency Platform
www.ecommdev.com.br - Bilingual (PT-BR / EN)
"""

from datetime import timedelta
from pathlib import Path

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY: Default to False (fail closed) to prevent accidental debug exposure
DEBUG = config('DEBUG', default=False, cast=bool)

# SECRET_KEY: Required in production, uses dev key only in DEBUG mode
_DEFAULT_DEV_KEY = 'django-insecure-dev-only-key-do-not-use-in-production'
SECRET_KEY = config('SECRET_KEY', default=_DEFAULT_DEV_KEY if DEBUG else '')

# Fail fast if SECRET_KEY not set in production
if not SECRET_KEY and not DEBUG:
    raise ValueError(
        "SECRET_KEY environment variable is required in production. "
        "Generate one with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    )

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Validate ALLOWED_HOSTS entries to catch misconfiguration early.
# Accepts: hostnames, FQDNs, IP addresses, '*' (wildcard — dev only), and '.domain.com' prefixes.
import re as _re

def _is_valid_allowed_host(host: str) -> bool:
    """Return True if host is a plausible ALLOWED_HOSTS entry."""
    if host == '*':
        return True  # Wildcard — allowed but only safe in DEBUG
    # Leading dot for subdomain wildcard (.example.com)
    _h = host.lstrip('.')
    # IPv4 address
    if _re.match(r'^\d{1,3}(\.\d{1,3}){3}$', _h):
        return True
    # IPv6 address (bracket notation or plain)
    if _h.startswith('[') or ':' in _h:
        return True
    # Hostname / FQDN: letters, digits, hyphens, dots
    if _re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]{0,251}[a-zA-Z0-9])?$', _h):
        return True
    return False

_invalid_hosts = [h for h in ALLOWED_HOSTS if not _is_valid_allowed_host(h)]
if _invalid_hosts:
    raise ValueError(
        f"ALLOWED_HOSTS contains invalid entries: {_invalid_hosts}. "
        "Each entry must be a valid hostname, IP address, or '*'."
    )

# Warn if wildcard is used outside DEBUG mode (fail-safe, not hard failure)
if '*' in ALLOWED_HOSTS and not DEBUG:
    import warnings as _warnings
    _warnings.warn(
        "ALLOWED_HOSTS contains '*' while DEBUG=False. "
        "This is a security risk — set explicit hostnames in production.",
        stacklevel=2,
    )

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',      # XML sitemap framework
    'django.contrib.sites',         # Required for sitemaps

    # Third Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local Apps
    'core.apps.CoreConfig',
    'servicos.apps.ServicosConfig',
    'pacotes.apps.PacotesConfig',
    'orcamentos.apps.OrcamentosConfig',
    'portfolio.apps.PortfolioConfig',
    'clientes.apps.ClientesConfig',
    'projetos.apps.ProjetosConfig',
    'suporte.apps.SuporteConfig',
    'faturas.apps.FaturasConfig',
    'notificacoes.apps.NotificacoesConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    # Security middleware (should be first)
    'django.middleware.security.SecurityMiddleware',
    # GZipMiddleware must come BEFORE WhiteNoise/static serving and AFTER SecurityMiddleware.
    # Placing it second ensures:
    #   1. Security checks (HTTPS redirect, HSTS headers) run before compression.
    #   2. All downstream responses (HTML, JSON, API) are compressed transparently.
    #   3. It wraps the full response stack, maximising bytes saved on the wire.
    # NOTE: Never place GZipMiddleware before SecurityMiddleware — it could mask
    # response headers that security checks rely on.
    'django.middleware.gzip.GZipMiddleware',
    'core.middleware.RequestValidationMiddleware',  # Block malicious requests early

    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom security middleware (after auth)
    'core.middleware.SecurityHeadersMiddleware',  # CSP and security headers
    'core.middleware.SessionSecurityMiddleware',  # Session hardening
    'core.middleware.LoggingMiddleware',  # Security logging
]

ROOT_URLCONF = 'ecommdev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # APP_DIRS must be False when using custom 'loaders'
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.site_settings',
                'core.seo.seo_context',             # SEO meta tags for all pages
            ],
            # Template caching: use cached.Loader in production for major speedup
            # In development: plain loaders (templates reload on each request)
            # In production: cached.Loader wraps both loaders for ~10x faster rendering
            'loaders': (
                [('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ])]
                if not config('DEBUG', default=False, cast=bool)
                else [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            ),
        },
    },
]

WSGI_APPLICATION = 'ecommdev.wsgi.application'

# =============================================================================
# DATABASE
# =============================================================================

DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')

# Security: validate DB_ENGINE against allowlist to prevent injection attacks
# Note: Using if/raise instead of assert — assert is stripped with python -O
_ALLOWED_DB_ENGINES = ('django.db.backends.sqlite3', 'django.db.backends.postgresql')
if DB_ENGINE not in _ALLOWED_DB_ENGINES:
    raise ValueError(
        f"Invalid DB_ENGINE '{DB_ENGINE}'. "
        f"Must be one of: {', '.join(_ALLOWED_DB_ENGINES)}"
    )

if 'postgresql' in DB_ENGINE:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': config('DB_NAME', default='ecommdev_db'),
            'USER': config('DB_USER', default='ecommdev_user'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': 600,  # Connection pooling: keep DB connections open for 10 min
            'CONN_HEALTH_CHECKS': True,  # Verify connections before reuse (Django 4.1+)
            'OPTIONS': {
                'connect_timeout': 5,
                'options': '-c default_transaction_isolation=read committed',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / config('DB_NAME', default='db.sqlite3'),
            'CONN_MAX_AGE': 60,  # Limited pooling for SQLite
        }
    }

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

REDIS_URL = config('REDIS_URL', default='')

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {'max_connections': 50},
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'IGNORE_EXCEPTIONS': True,  # Degrade gracefully if Redis is down
            },
            'KEY_PREFIX': 'ecommdev',
            'TIMEOUT': 300,  # 5 min default TTL
        }
    }
    # Store sessions in Redis (fast + shared across workers)
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    # Fall back to DB-backed sessions without Redis
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    # Custom validators for additional security
    {'NAME': 'core.security.BreachedPasswordValidator'},
    {'NAME': 'core.security.SequentialCharacterValidator', 'OPTIONS': {'max_sequential': 4}},
    {'NAME': 'core.security.RepeatedCharacterValidator', 'OPTIONS': {'max_repeated': 3}},
]

# =============================================================================
# INTERNATIONALIZATION (i18n)
# =============================================================================

LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')
TIME_ZONE = config('TIME_ZONE', default='America/Fortaleza')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('pt-br', 'Portugues (Brasil)'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

AUTH_USER_MODEL = 'clientes.Usuario'

# =============================================================================
# AUTHENTICATION
# =============================================================================

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# =============================================================================
# REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    # Security (3.3): Disable DRF browsable API in production to prevent
    # information leakage and reduce attack surface. Only JSONRenderer is
    # exposed in production; BrowsableAPIRenderer is available in DEBUG mode.
    'DEFAULT_RENDERER_CLASSES': (
        [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ]
        if DEBUG
        else [
            'rest_framework.renderers.JSONRenderer',
        ]
    ),
}

# =============================================================================
# JWT SETTINGS
# =============================================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('JWT_REFRESH_TOKEN_LIFETIME', default=10080, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# =============================================================================
# CORS SETTINGS
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    'https://www.ecommdev.com.br',
    'https://ecommdev.com.br',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.ecommdev.com.br',
    'https://ecommdev.com.br',
    'https://mrdev02.pythonanywhere.com',
]

# =============================================================================
# EMAIL SETTINGS
# =============================================================================

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='ECOMMDEV <contato@ecommdev.com.br>')

# =============================================================================
# RATE LIMITING - Trusted Proxy Configuration
# =============================================================================
# SECURITY: Configure these settings if your app is behind a reverse proxy
# (e.g., Nginx, Cloudflare, AWS ALB) to prevent IP spoofing attacks.

# List of trusted proxy IPs that are allowed to set X-Forwarded-For
# Example: ['10.0.0.1', '172.16.0.0/12'] or use environment variable
TRUSTED_PROXY_IPS = config(
    'TRUSTED_PROXY_IPS',
    default='',
    cast=lambda v: [ip.strip() for ip in v.split(',') if ip.strip()]
)

# Number of trusted proxies in the chain
# If you have: Client -> Cloudflare -> Nginx -> App, set to 2
NUM_TRUSTED_PROXIES = config('NUM_TRUSTED_PROXIES', default=1, cast=int)

# =============================================================================
# SECURITY SETTINGS (Production)
# =============================================================================

# SECURITY: Apply HttpOnly and SameSite cookie flags in ALL environments
# (including DEBUG=True) to protect sessions even during development.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

if not DEBUG:
    # HTTPS/SSL Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Content Security
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    # Additional Security Headers
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

    # Session expiration (2 hours of inactivity)
    SESSION_COOKIE_AGE = 7200
    SESSION_SAVE_EVERY_REQUEST = True  # Reset expiry on each request
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False

    # Session rotation interval (seconds) - used by SessionSecurityMiddleware
    SESSION_ROTATION_INTERVAL = 1800  # 30 minutes

# =============================================================================
# SITE SETTINGS
# =============================================================================

SITE_URL = config('SITE_URL', default='http://localhost:8000')
SITE_NAME = 'ECOMMDEV'
SITE_DESCRIPTION = 'Desenvolvimento Web Profissional para Pequenas e Medias Empresas'

# django.contrib.sites framework
SITE_ID = 1

# =============================================================================
# PAYMENT SETTINGS (Mercado Pago)
# =============================================================================

MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN', default='')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY', default='')
MERCADOPAGO_WEBHOOK_SECRET = config('MERCADOPAGO_WEBHOOK_SECRET', default='')

# =============================================================================
# ANALYTICS
# =============================================================================

GA_TRACKING_ID = config('GA_TRACKING_ID', default='')

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# =============================================================================
# ERROR REPORTING — Sentry (disabled by default; enable in production)
# =============================================================================
# To enable:
#   1. pip install sentry-sdk
#   2. Add sentry-sdk to requirements.txt
#   3. Set SENTRY_DSN in your .env file
#   4. Uncomment the block below
#
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.redis import RedisIntegration
#
# SENTRY_DSN = config('SENTRY_DSN', default='')
# if SENTRY_DSN:
#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[
#             DjangoIntegration(
#                 transaction_style='url',
#                 middleware_spans=True,
#                 signals_spans=True,
#             ),
#             RedisIntegration(),
#         ],
#         traces_sample_rate=config('SENTRY_TRACES_SAMPLE_RATE', default=0.1, cast=float),
#         send_default_pii=False,   # Do NOT send PII (emails, IPs) to Sentry
#         environment=config('SENTRY_ENVIRONMENT', default='production'),
#         release=config('GIT_COMMIT_SHA', default='unknown'),
#     )
