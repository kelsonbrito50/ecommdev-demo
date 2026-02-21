"""URL patterns for products app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'products'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
