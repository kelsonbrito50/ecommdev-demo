"""Pacotes app URLs."""

from django.urls import path

from . import views

app_name = "pacotes"

urlpatterns = [
    path("", views.PacoteListView.as_view(), name="lista"),
    path("<str:tipo>/", views.PacoteDetailView.as_view(), name="detalhe"),
]
