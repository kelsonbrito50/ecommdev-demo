"""URL patterns for analytics app."""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('revenue/', views.RevenueByPeriodView.as_view(), name='revenue'),
]
