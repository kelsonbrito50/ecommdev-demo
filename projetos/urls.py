"""Projetos app URLs."""
from django.urls import path
from . import views

app_name = 'projetos'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('projetos/', views.ProjetoListView.as_view(), name='lista'),
    path('projetos/<slug:slug>/', views.ProjetoDetailView.as_view(), name='detalhe'),
    path('projetos/<slug:slug>/mensagens/', views.MensagensView.as_view(), name='mensagens'),
    path('projetos/<slug:slug>/arquivos/', views.ArquivosView.as_view(), name='arquivos'),
    path('projetos/<slug:slug>/timeline/', views.TimelineView.as_view(), name='timeline'),
    path('projetos/<slug:slug>/mensagens/enviar/', views.EnviarMensagemView.as_view(), name='enviar_mensagem'),
]
