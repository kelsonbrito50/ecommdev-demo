"""URL patterns for payments app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'payments'

router = DefaultRouter()
router.register('', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('create/', views.CreatePaymentView.as_view(), name='create'),
    path('webhook/', views.WebhookView.as_view(), name='webhook'),
    path('', include(router.urls)),
]
