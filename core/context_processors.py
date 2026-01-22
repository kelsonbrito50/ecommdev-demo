"""
Core context processors for site-wide data.
"""
from django.conf import settings


def site_settings(request):
    """Add site settings to all templates."""
    from core.models import ConfiguracaoSite

    try:
        config = ConfiguracaoSite.objects.first()
    except Exception:
        config = None

    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'GA_TRACKING_ID': settings.GA_TRACKING_ID,
        'config': config,
        'current_language': request.LANGUAGE_CODE if hasattr(request, 'LANGUAGE_CODE') else 'pt-br',
    }
