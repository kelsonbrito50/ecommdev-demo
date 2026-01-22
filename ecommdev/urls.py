"""
ECOMMDEV URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# API URLs (no language prefix)
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

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
