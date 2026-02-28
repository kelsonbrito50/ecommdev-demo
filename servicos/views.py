"""Servicos app views."""

from django.views.generic import DetailView, ListView

from .models import Servico


class ServicoListView(ListView):
    """List all services."""

    model = Servico
    template_name = "servicos/lista.html"
    context_object_name = "servicos"
    queryset = Servico.objects.filter(ativo=True)


class ServicoDetailView(DetailView):
    """Service detail page."""

    model = Servico
    template_name = "servicos/detalhe.html"
    context_object_name = "servico"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Servico.objects.filter(ativo=True)
