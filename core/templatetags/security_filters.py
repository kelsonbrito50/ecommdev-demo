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

    SECURITY (8.2): Uses nh3 (Rust-backed ammonia) instead of the deprecated
    bleach library.  nh3 does not support '*' wildcard attributes directly,
    so the wildcard set is merged into each individual tag's attribute set.

    Usage: {{ content|sanitize_html }}
    """
    if not value:
        return ''

    import nh3

    # Build per-tag attribute allowlist.  nh3 does not support the '*' wildcard
    # key directly, so we expand it: every allowed tag gets the wildcard attrs
    # merged with its own tag-specific attrs.
    wildcard_attrs = ALLOWED_ATTRIBUTES.get('*', set())
    allowed_attrs: dict[str, set[str]] = {}
    for tag in ALLOWED_TAGS:
        tag_attrs = set(ALLOWED_ATTRIBUTES.get(tag, set())) | wildcard_attrs
        if tag_attrs:
            allowed_attrs[tag] = tag_attrs

    # nh3.clean strips unknown tags and attributes by default (no strip= param needed).
    # url_schemes restricts href/src to safe protocols only.
    cleaned = nh3.clean(
        str(value),
        tags=set(ALLOWED_TAGS),
        attributes=allowed_attrs,
        url_schemes={'http', 'https', 'mailto'},
        strip_comments=True,
    )

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
