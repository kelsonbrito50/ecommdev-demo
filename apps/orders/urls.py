"""URL patterns for orders app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'orders'

router = DefaultRouter()
router.register('items', views.CartItemViewSet, basename='cart-item')
router.register('history', views.OrderViewSet, basename='order')

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/', include(router.urls)),
    path('checkout/', views.CreateOrderView.as_view(), name='checkout'),
]
