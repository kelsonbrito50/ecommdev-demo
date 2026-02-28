"""Suporte app URLs."""

from django.urls import path

from . import views

app_name = "suporte"

urlpatterns = [
    path("", views.TicketListView.as_view(), name="lista"),
    path("novo/", views.TicketCreateView.as_view(), name="criar"),
    path("<str:numero>/", views.TicketDetailView.as_view(), name="detalhe"),
    path("<str:numero>/responder/", views.TicketRespostaView.as_view(), name="responder"),
    path("<str:numero>/avaliar/", views.TicketAvaliacaoView.as_view(), name="avaliar"),
]
