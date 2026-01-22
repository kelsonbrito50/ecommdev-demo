"""
File upload validators for security.
Validates file types, sizes, and content to prevent malicious uploads.
"""
import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Maximum file sizes
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2 MB

# Allowed extensions
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv'}
ALLOWED_AVATAR_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Image file signatures (magic bytes)
IMAGE_SIGNATURES = {
    b'\xff\xd8\xff': 'jpeg',
    b'\x89PNG\r\n\x1a\n': 'png',
    b'GIF87a': 'gif',
    b'GIF89a': 'gif',
    b'RIFF': 'webp',
}

# Document file signatures
DOCUMENT_SIGNATURES = {
    b'%PDF': 'pdf',
    b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'doc',  # MS Office old format
    b'PK\x03\x04': 'docx',  # ZIP-based (docx, xlsx)
}


def validate_file_extension(file, allowed_extensions):
    """Validate file has an allowed extension."""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            _('Tipo de arquivo não permitido. Extensões permitidas: %(extensions)s'),
            params={'extensions': ', '.join(sorted(allowed_extensions))},
            code='invalid_extension'
        )
    return ext


def validate_file_size(file, max_size):
    """Validate file doesn't exceed maximum size."""
    if file.size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(
            _('Arquivo muito grande. Tamanho máximo: %(max_size).1f MB'),
            params={'max_size': max_mb},
            code='file_too_large'
        )


def validate_file_content(file, signatures):
    """
    Validate file content matches expected type by checking magic bytes.
    This prevents uploading malicious files with renamed extensions.
    """
    # Read first bytes to check signature
    file.seek(0)
    header = file.read(16)
    file.seek(0)  # Reset file pointer

    for sig, file_type in signatures.items():
        if header.startswith(sig):
            return file_type

    return None


class ImageValidator:
    """
    Validator for image uploads.
    Checks extension, size, and content signature.
    """

    def __init__(self, max_size=MAX_IMAGE_SIZE, allowed_extensions=None):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or ALLOWED_IMAGE_EXTENSIONS

    def __call__(self, file):
        # Validate extension
        ext = validate_file_extension(file, self.allowed_extensions)

        # Validate size
        validate_file_size(file, self.max_size)

        # Validate content signature for images
        detected_type = validate_file_content(file, IMAGE_SIGNATURES)

        # Check if extension matches content
        ext_type_map = {
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
            '.webp': 'webp',
        }

        expected_type = ext_type_map.get(ext)
        if expected_type and detected_type and detected_type != expected_type:
            raise ValidationError(
                _('Conteúdo do arquivo não corresponde à extensão.'),
                code='content_mismatch'
            )


class DocumentValidator:
    """
    Validator for document uploads.
    Checks extension and size.
    """

    def __init__(self, max_size=MAX_DOCUMENT_SIZE, allowed_extensions=None):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or ALLOWED_DOCUMENT_EXTENSIONS

    def __call__(self, file):
        # Validate extension
        validate_file_extension(file, self.allowed_extensions)

        # Validate size
        validate_file_size(file, self.max_size)


class AvatarValidator:
    """
    Stricter validator for user profile photos.
    Smaller size limit and fewer allowed formats.
    """

    def __init__(self, max_size=MAX_AVATAR_SIZE, allowed_extensions=None):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or ALLOWED_AVATAR_EXTENSIONS

    def __call__(self, file):
        # Validate extension
        ext = validate_file_extension(file, self.allowed_extensions)

        # Validate size
        validate_file_size(file, self.max_size)

        # Validate content signature
        detected_type = validate_file_content(file, IMAGE_SIGNATURES)

        ext_type_map = {
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.png': 'png',
        }

        expected_type = ext_type_map.get(ext)
        if expected_type and detected_type and detected_type != expected_type:
            raise ValidationError(
                _('Conteúdo do arquivo não corresponde à extensão.'),
                code='content_mismatch'
            )


# Convenience instances
validate_image = ImageValidator()
validate_document = DocumentValidator()
validate_avatar = AvatarValidator()
