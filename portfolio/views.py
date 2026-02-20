"""Portfolio app views."""
from django.views.generic import ListView, DetailView
from .models import Case, CategoriaPortfolio


class CaseListView(ListView):
    """List all portfolio cases."""
    model = Case
    template_name = 'portfolio/lista.html'
    context_object_name = 'cases'
    queryset = Case.objects.filter(ativo=True)
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaPortfolio.objects.all()
        return context


class CaseDetailView(DetailView):
    """Case study detail page."""
    model = Case
    template_name = 'portfolio/detalhe.html'
    context_object_name = 'case'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Case.objects.filter(ativo=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        from django.db.models import F
        Case.objects.filter(pk=obj.pk).update(visualizacoes=F('visualizacoes') + 1)
        obj.visualizacoes += 1  # Update in-memory for the current request
        return obj
