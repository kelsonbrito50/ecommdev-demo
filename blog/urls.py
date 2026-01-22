"""Blog app URLs."""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='lista'),
    path('categoria/<slug:slug>/', views.CategoriaPostListView.as_view(), name='categoria'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='detalhe'),
]
