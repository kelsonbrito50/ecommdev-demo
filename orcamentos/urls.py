"""Orcamentos app URLs."""
from django.urls import path
from . import views

app_name = 'orcamentos'

urlpatterns = [
    path('', views.OrcamentoCreateView.as_view(), name='criar'),
    path('sucesso/', views.OrcamentoSucessoView.as_view(), name='sucesso'),
    path('meus/', views.MeusOrcamentosView.as_view(), name='meus'),
]
