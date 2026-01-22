"""Servicos app URLs."""
from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.ServicoListView.as_view(), name='lista'),
    path('<slug:slug>/', views.ServicoDetailView.as_view(), name='detalhe'),
]
