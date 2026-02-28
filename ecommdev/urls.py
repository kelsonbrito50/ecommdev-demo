"""
ECOMMDEV URL Configuration
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.webhook import github_webhook
from core.sitemaps import sitemaps
from faturas.views import MercadoPagoWebhookView


class AdminLogoutView(TemplateView):
    """Custom admin logout view - logs out immediately."""

    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        return redirect('admin:login')

    def post(self, request):
        from django.contrib.auth import logout
        logout(request)
        return redirect('admin:login')

# robots.txt view
def robots_txt(request):
    site_url = settings.SITE_URL
    content = f"""User-agent: *
Allow: /
Disallow: /gerenciar-ecd/
Disallow: /api/
Disallow: /dashboard/
Disallow: /suporte/
Disallow: /faturas/
Disallow: /orcamento/
Disallow: /login/
Disallow: /registro/

# Sitemap
Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


# API URLs (no language prefix)
urlpatterns = [
    # SEO files (must be at root, no language prefix)
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # Webhooks (outside i18n prefix)
    path('webhook/github/', github_webhook, name='github_webhook'),
    path('webhook/mercadopago/', MercadoPagoWebhookView.as_view(), name='webhook_mp_global'),

    # Admin logout (custom view for GET support)
    path('gerenciar-ecd/logout/', AdminLogoutView.as_view(), name='admin_logout'),

    # Admin (obscured URL for security)
    path('gerenciar-ecd/', admin.site.urls),

    # API v1
    path('api/v1/', include('api.urls')),

    # JWT Auth
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Language selection
    path('i18n/', include('django.conf.urls.i18n')),
]

# i18n URLs (with language prefix)
urlpatterns += i18n_patterns(
    # Core pages
    path('', include('core.urls')),

    # Services
    path('servicos/', include('servicos.urls')),

    # Packages
    path('pacotes/', include('pacotes.urls')),

    # Quote requests
    path('orcamento/', include('orcamentos.urls')),

    # Portfolio
    path('portfolio/', include('portfolio.urls')),

    # Client area
    path('', include('clientes.urls')),

    # Dashboard / Projects
    path('dashboard/', include('projetos.urls')),

    # Support
    path('suporte/', include('suporte.urls')),

    # Invoices
    path('faturas/', include('faturas.urls')),

    prefix_default_language=False,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = 'ECOMMDEV Admin'
admin.site.site_title = 'ECOMMDEV'
admin.site.index_title = 'Painel Administrativo'

# Custom error handlers
handler400 = 'core.views.error_400'
handler403 = 'core.views.error_403'
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
