"""Pacotes app views."""

from django.views.generic import DetailView, ListView

from .models import Pacote


class PacoteListView(ListView):
    """List all packages."""

    model = Pacote
    template_name = "pacotes/lista.html"
    context_object_name = "pacotes"
    queryset = Pacote.objects.filter(ativo=True)


class PacoteDetailView(DetailView):
    """Package detail page."""

    model = Pacote
    template_name = "pacotes/detalhe.html"
    context_object_name = "pacote"
    slug_field = "tipo"
    slug_url_kwarg = "tipo"
    queryset = Pacote.objects.filter(ativo=True)
