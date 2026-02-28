"""
Security utilities and validators.
"""
import hashlib
import hmac
import logging
import secrets
import string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def generate_secure_token(length=32):
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def generate_secure_password(length=16):
    """Generate a secure random password with mixed characters."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def constant_time_compare(val1, val2):
    """
    Compare two strings in constant time to prevent timing attacks.
    Uses hmac.compare_digest internally.
    """
    return hmac.compare_digest(str(val1), str(val2))


def hash_sensitive_data(data, salt=None):
    """
    Hash sensitive data for logging/storage where original isn't needed.
    Uses SHA-256 with optional salt.
    """
    if salt:
        data = f"{salt}:{data}"
    return hashlib.sha256(data.encode()).hexdigest()


class BreachedPasswordValidator:
    """
    Validate that password is not in a list of commonly breached passwords.

    This is a basic implementation that checks against a local list.
    For production, consider integrating with Have I Been Pwned API.
    """

    # Common breached passwords (subset - extend as needed)
    COMMON_PASSWORDS = {
        '123456', '123456789', 'qwerty', 'password', '12345678',
        '111111', '1234567890', '1234567', 'password1', '123123',
        'abc123', '1234', 'iloveyou', '000000', 'password123',
        'admin', 'letmein', 'welcome', 'monkey', 'dragon',
        'master', 'login', 'sunshine', 'princess', 'qwerty123',
        'senha', 'senha123', '123mudar', 'mudar123', 'brasil',
        # Add Portuguese common passwords
        'amor', 'familia', 'futebol', 'deus', 'jesus',
    }

    def validate(self, password, user=None):
        if password.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                _('Esta senha é muito comum e foi encontrada em vazamentos de dados. '
                  'Por favor, escolha uma senha mais segura.'),
                code='password_breached',
            )

    def get_help_text(self):
        return _('Sua senha não pode ser uma senha comumente usada ou vazada.')


class SequentialCharacterValidator:
    """
    Validate that password doesn't contain sequential characters.
    Prevents passwords like 'abcdef' or '123456'.
    """

    def __init__(self, max_sequential=3):
        self.max_sequential = max_sequential

    def validate(self, password, user=None):
        sequential_count = 1
        for i in range(1, len(password)):
            if ord(password[i]) == ord(password[i-1]) + 1:
                sequential_count += 1
                if sequential_count > self.max_sequential:
                    raise ValidationError(
                        _('Sua senha não pode conter mais de %(max)d caracteres sequenciais.'),
                        code='password_sequential',
                        params={'max': self.max_sequential},
                    )
            else:
                sequential_count = 1

    def get_help_text(self):
        # Use % formatting AFTER _() so gettext can extract the static template string.
        # f-strings inside _() produce dynamic strings that confuse translation tools.
        return _('Sua senha não pode conter mais de %(max)d caracteres sequenciais (ex: abc, 123).') % {
            'max': self.max_sequential
        }


class RepeatedCharacterValidator:
    """
    Validate that password doesn't have too many repeated characters.
    Prevents passwords like 'aaaaaa' or '111111'.
    """

    def __init__(self, max_repeated=3):
        self.max_repeated = max_repeated

    def validate(self, password, user=None):
        repeated_count = 1
        for i in range(1, len(password)):
            if password[i] == password[i-1]:
                repeated_count += 1
                if repeated_count > self.max_repeated:
                    raise ValidationError(
                        _('Sua senha não pode conter mais de %(max)d caracteres repetidos consecutivos.'),
                        code='password_repeated',
                        params={'max': self.max_repeated},
                    )
            else:
                repeated_count = 1

    def get_help_text(self):
        # Use % formatting AFTER _() so gettext can extract the static template string.
        return _('Sua senha não pode conter mais de %(max)d caracteres repetidos consecutivos.') % {
            'max': self.max_repeated
        }


def sanitize_filename(filename):
    """
    Sanitize a filename to prevent path traversal and other attacks.
    """
    import os
    import re
    import unicodedata

    # Normalize unicode characters
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')

    # Remove path components
    filename = os.path.basename(filename)

    # Remove null bytes
    filename = filename.replace('\x00', '')

    # Replace suspicious characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)

    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext

    return filename or 'unnamed'


def mask_email(email):
    """Mask email for display: t***@e***.com"""
    if not email or '@' not in email:
        return '***@***.***'

    local, domain = email.rsplit('@', 1)
    domain_parts = domain.rsplit('.', 1)

    masked_local = local[0] + '***' if local else '***'
    masked_domain = domain_parts[0][0] + '***' if domain_parts[0] else '***'

    if len(domain_parts) > 1:
        return f"{masked_local}@{masked_domain}.{domain_parts[1]}"
    return f"{masked_local}@{masked_domain}"


def mask_phone(phone):
    """Mask phone for display: (**) *****-1234"""
    if not phone:
        return '(**) *****-****'

    # Keep only digits
    digits = ''.join(c for c in phone if c.isdigit())

    if len(digits) >= 4:
        return f'(**) *****-{digits[-4:]}'
    return '(**) *****-****'
