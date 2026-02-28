"""API v1 URLs."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import health_check

router = DefaultRouter()
router.register(r"servicos", views.ServicoViewSet, basename="servico")
router.register(r"pacotes", views.PacoteViewSet, basename="pacote")
router.register(r"portfolio", views.CaseViewSet, basename="case")
router.register(r"orcamentos", views.OrcamentoViewSet, basename="orcamento")
router.register(r"projetos", views.ProjetoViewSet, basename="projeto")
router.register(r"tickets", views.TicketViewSet, basename="ticket")
router.register(r"faturas", views.FaturaViewSet, basename="fatura")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    # Health check (no auth required — used by Docker/load balancers)
    path("health/", health_check, name="health_check"),
    # Client profile
    path("clientes/me/", views.ClienteProfileView.as_view(), name="cliente_profile"),
    # Contact
    path("contato/", views.ContatoCreateView.as_view(), name="contato"),
    # Notifications
    path("notificacoes/", views.NotificacaoListView.as_view(), name="notificacoes"),
    path(
        "notificacoes/<int:pk>/lida/",
        views.NotificacaoMarcarLidaView.as_view(),
        name="notificacao_lida",
    ),
]
