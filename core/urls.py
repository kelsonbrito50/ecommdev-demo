"""Core app URLs."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("sobre/", views.SobreView.as_view(), name="sobre"),
    path("contato/", views.ContatoView.as_view(), name="contato"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("termos/", views.TermosView.as_view(), name="termos"),
    path("privacidade/", views.PrivacidadeView.as_view(), name="privacidade"),
]
