"""
Security template filters for HTML sanitization.
Provides XSS protection while allowing safe HTML formatting.
"""
import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

# Allowed HTML tags for content
ALLOWED_TAGS = {
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li',
    'a', 'img',
    'blockquote', 'pre', 'code',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span',
    'hr',
}

# Allowed attributes per tag
ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title', 'target', 'rel'},
    'img': {'src', 'alt', 'title', 'width', 'height'},
    '*': {'class', 'id'},
}

# Dangerous patterns to remove
DANGEROUS_PATTERNS = [
    re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
    re.compile(r'<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL),
    re.compile(r'javascript:', re.IGNORECASE),
    re.compile(r'vbscript:', re.IGNORECASE),
    re.compile(r'on\w+\s*=', re.IGNORECASE),
    re.compile(r'expression\s*\(', re.IGNORECASE),
]


def strip_dangerous_content(html):
    """Remove dangerous HTML patterns."""
    if not html:
        return ''

    result = str(html)
    for pattern in DANGEROUS_PATTERNS:
        result = pattern.sub('', result)

    return result


@register.filter(name='sanitize_html')
def sanitize_html(value):
    """
    Sanitize HTML content to prevent XSS attacks.

    Removes script tags, event handlers, and other dangerous content
    while preserving safe formatting tags.

    SECURITY: This filter REQUIRES the bleach library. Regex-based
    sanitization is not secure and has been removed.

    Usage: {{ content|sanitize_html }}
    """
    if not value:
        return ''

    import bleach

    allowed_tags = list(ALLOWED_TAGS)
    allowed_attrs = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        '*': ['class', 'id'],
    }

    # Clean the HTML
    cleaned = bleach.clean(
        str(value),
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

    # Linkify URLs safely
    cleaned = bleach.linkify(cleaned)

    return mark_safe(cleaned)


@register.filter(name='safe_text')
def safe_text(value):
    """
    Escape all HTML - use for plain text that should never contain HTML.

    Usage: {{ user_input|safe_text }}
    """
    if not value:
        return ''
    return escape(str(value))
