# Security Audit Report - ECOMMDEV
**Date:** 2026-01-22
**Django Version:** 6.0.1
**Restore Point:** `restore-point-20260122-140931`

---

## Executive Summary

Overall security posture: **GOOD** with some improvements needed.

The application follows Django security best practices with proper authentication, CSRF protection, rate limiting, and secure production settings. However, several issues need attention before production deployment.

---

## Positive Findings (Security Strengths)

| Category | Status | Details |
|----------|--------|---------|
| SQL Injection | PROTECTED | Uses Django ORM exclusively, no raw SQL |
| XSS | PROTECTED | Templates use auto-escaping, no `\|safe` or `mark_safe` |
| CSRF | PROTECTED | CsrfViewMiddleware enabled, tokens required |
| Password Security | STRONG | 4 validators, min 8 chars, complexity rules |
| Rate Limiting | IMPLEMENTED | Custom limiter on login (5/min), register (3/min) |
| Production Security | CONFIGURED | HSTS, secure cookies, SSL redirect when DEBUG=False |
| API Security | CONFIGURED | JWT auth, throttling (100/h anon, 1000/h user) |
| Session Security | GOOD | Session auth hash updated on password change |
| Webhook Security | PARTIAL | HMAC signature verification implemented |

---

## Critical Issues

### 1. CRITICAL: GitHub Webhook Executes Without Secret Verification

**File:** `core/webhook.py:19-31`

**Risk:** Remote Code Execution via deploy script if webhook URL is discovered

**Current Code:**
```python
secret = getattr(settings, 'GITHUB_WEBHOOK_SECRET', None)
if secret:  # Only verifies if secret exists
    # ... verification code
# Proceeds to execute deploy script regardless
```

**Fix Required:** Block execution if no secret configured

---

### 2. HIGH: Insecure Default SECRET_KEY

**File:** `ecommdev/settings.py:19`

**Risk:** Predictable session tokens, CSRF bypass

**Current Code:**
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
```

**Fix Required:** Remove default, fail if not set in production

---

## High Priority Issues

### 3. Admin at Predictable URL

**File:** `ecommdev/urls.py:18`

**Risk:** Easier brute-force attacks on admin login

**Current:** `/admin/`

**Recommendation:** Use obscure URL like `/manage-xyz123/`

---

### 4. File Upload Validation Missing

**Files:** Multiple models with ImageField/FileField

**Risk:** Malicious file uploads, storage exhaustion

**Affected:**
- `clientes/models.py:47` - User photos
- `servicos/models.py:38` - Service images
- `portfolio/models.py:72,165` - Portfolio images
- `projetos/models.py:223` - Project files
- `core/models.py:19,26,106` - Site assets

**Fix Required:** Add file type and size validation

---

### 5. MercadoPago Webhook Security Gap

**File:** `faturas/views.py:107-113`

**Risk:** Fake payment notifications could be processed

**Current Code:**
```python
if not webhook_secret:
    logger.warning(...)
    return False  # Returns False but continues processing
```

**Fix Required:** Block request if secret not configured

---

## Medium Priority Issues

### 6. X-Forwarded-For Header Spoofing

**File:** `core/ratelimit.py:13-18`

**Risk:** Rate limit bypass by spoofing IP

**Recommendation:** Validate against trusted proxy list

---

### 7. Debug Toolbar in Dependencies

**File:** `requirements.txt`

**Risk:** Information disclosure if enabled in production

**Recommendation:** Move to dev-only requirements

---

## Recommended Fixes

### Fix 1: Secure Webhook (core/webhook.py)

```python
@csrf_exempt
@require_POST
def github_webhook(request):
    """Handle GitHub webhook for auto-deployment"""
    secret = getattr(settings, 'GITHUB_WEBHOOK_SECRET', None)

    # SECURITY: Require secret in production
    if not secret:
        if not settings.DEBUG:
            return HttpResponseForbidden('Webhook secret not configured')
        # Allow in development with warning
        import logging
        logging.warning("GITHUB_WEBHOOK_SECRET not set - skipping verification")
    else:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            return HttpResponseForbidden('Missing signature')

        expected = 'sha256=' + hmac.new(
            secret.encode(),
            request.body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            return HttpResponseForbidden('Invalid signature')

    # Rest of deployment code...
```

### Fix 2: Secure SECRET_KEY (settings.py)

```python
SECRET_KEY = config('SECRET_KEY')  # No default - will raise if not set
```

### Fix 3: Obscure Admin URL (urls.py)

```python
path('manage-ecd2026/', admin.site.urls),  # Change to random path
```

### Fix 4: File Upload Validators (create validators.py)

```python
# core/validators.py
from django.core.exceptions import ValidationError

def validate_image_file(value):
    """Validate uploaded image files."""
    import os
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file type.')

    # Max 5MB
    if value.size > 5 * 1024 * 1024:
        raise ValidationError('File too large. Max 5MB.')

def validate_document_file(value):
    """Validate uploaded document files."""
    import os
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file type.')

    # Max 10MB
    if value.size > 10 * 1024 * 1024:
        raise ValidationError('File too large. Max 10MB.')
```

### Fix 5: Secure MercadoPago Webhook (faturas/views.py)

```python
def _verify_signature(self, request, data):
    webhook_secret = getattr(settings, 'MERCADOPAGO_WEBHOOK_SECRET', None)

    if not webhook_secret:
        logger.error("MERCADOPAGO_WEBHOOK_SECRET not configured!")
        return False  # Block if no secret

    # Continue with signature verification...
```

---

## Security Headers Recommendation

Add to `settings.py` for production:

```python
if not DEBUG:
    # ... existing settings ...

    # Content Security Policy (via middleware or django-csp)
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
    CSP_SCRIPT_SRC = ("'self'", "https://cdn.jsdelivr.net")
    CSP_IMG_SRC = ("'self'", "data:", "https:")

    # Additional headers
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    PERMISSIONS_POLICY = {
        "geolocation": [],
        "microphone": [],
        "camera": [],
    }
```

---

## Checklist Before Production

- [ ] Set strong SECRET_KEY in .env (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Set DEBUG=False
- [ ] Configure GITHUB_WEBHOOK_SECRET
- [ ] Configure MERCADOPAGO_WEBHOOK_SECRET
- [ ] Change admin URL from /admin/
- [ ] Add file upload validators
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Review CORS_ALLOWED_ORIGINS
- [ ] Set up proper email backend (not console)
- [ ] Configure error logging/monitoring (Sentry)
- [ ] Remove django-debug-toolbar from production

---

## Restore Point

To revert changes if needed:
```bash
git checkout restore-point-20260122-140931
```

---

**Report Generated:** 2026-01-22 14:XX BRT
