"""Portfolio app URLs."""

from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.CaseListView.as_view(), name="lista"),
    path("<slug:slug>/", views.CaseDetailView.as_view(), name="detalhe"),
]
