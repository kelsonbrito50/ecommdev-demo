"""
XML Sitemap configuration for ECOMMDEV.
Covers static pages, portfolio cases, and services.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime


class StaticViewSitemap(Sitemap):
    """Sitemap for static/informational pages.

    Priority and changefreq are set per-item via methods below,
    so no class-level defaults are needed (they would be shadowed).
    """
    protocol = 'https'

    # (url_name, priority_override)
    pages = [
        ('core:home', 1.0, 'daily'),
        ('core:sobre', 0.7, 'monthly'),
        ('core:contato', 0.8, 'monthly'),
        ('core:faq', 0.6, 'monthly'),
        ('servicos:lista', 0.9, 'weekly'),
        ('pacotes:lista', 0.9, 'weekly'),
        ('portfolio:lista', 0.8, 'weekly'),
        ('orcamentos:criar', 0.8, 'monthly'),
        ('core:termos', 0.3, 'yearly'),
        ('core:privacidade', 0.3, 'yearly'),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        url_name, priority, changefreq = item
        try:
            return reverse(url_name)
        except Exception:
            return '/'

    def priority(self, item):
        url_name, priority, changefreq = item
        return priority

    def changefreq(self, item):
        url_name, priority, changefreq = item
        return changefreq


class PortfolioSitemap(Sitemap):
    """Sitemap for portfolio case studies."""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        try:
            from portfolio.models import Case
            return Case.objects.filter(ativo=True).order_by('-updated_at')
        except Exception:
            return []

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ServicesSitemap(Sitemap):
    """Sitemap for individual service pages."""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        try:
            from servicos.models import Servico
            return Servico.objects.filter(ativo=True).order_by('ordem')
        except Exception:
            return []

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


# Registry used in urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'portfolio': PortfolioSitemap,
    'servicos': ServicesSitemap,
}
