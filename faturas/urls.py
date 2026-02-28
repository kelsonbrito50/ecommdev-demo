"""Faturas app URLs."""

from django.urls import path

from . import views

app_name = "faturas"

urlpatterns = [
    path("", views.FaturaListView.as_view(), name="lista"),
    path("<str:numero>/", views.FaturaDetailView.as_view(), name="detalhe"),
    path("<str:numero>/pagar/", views.FaturaPagarView.as_view(), name="pagar"),
    path("<str:numero>/pdf/", views.FaturaPDFView.as_view(), name="pdf"),
    path("webhook/mercadopago/", views.MercadoPagoWebhookView.as_view(), name="webhook_mp"),
]
