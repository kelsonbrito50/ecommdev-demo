"""Projetos app views."""
import bleach
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Projeto, MensagemProjeto, ArquivoProjeto, TimelineEvento
from faturas.models import Fatura
from suporte.models import Ticket
from orcamentos.models import Orcamento

# Security (3.4): Allowed HTML tags and attributes for project messages.
# Rich formatting is intentionally limited to prevent XSS.
_MSG_ALLOWED_TAGS = ['p', 'br', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'pre', 'code']
_MSG_ALLOWED_ATTRS = {}  # No attributes allowed in message content


class DashboardView(LoginRequiredMixin, TemplateView):
    """Client dashboard."""
    template_name = 'projetos/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['projetos'] = Projeto.objects.filter(cliente=user)[:5]
        context['projetos_ativos'] = Projeto.objects.filter(
            cliente=user,
            status__in=['em_desenvolvimento', 'em_testes', 'revisao']
        ).count()
        context['faturas_pendentes'] = Fatura.objects.filter(
            cliente=user,
            status='pendente'
        )
        context['tickets_abertos'] = Ticket.objects.filter(
            cliente=user,
            status__in=['aberto', 'em_atendimento']
        ).count()
        # Add orcamentos
        context['orcamentos'] = Orcamento.objects.filter(cliente=user)[:5]
        context['orcamentos_pendentes'] = Orcamento.objects.filter(
            cliente=user,
            status__in=['novo', 'em_analise', 'aguardando_info']
        ).count()
        return context


class ProjetoListView(LoginRequiredMixin, ListView):
    """List all client projects."""
    model = Projeto
    template_name = 'projetos/lista.html'
    context_object_name = 'projetos'

    def get_queryset(self):
        return Projeto.objects.filter(cliente=self.request.user)


class ProjetoDetailView(LoginRequiredMixin, DetailView):
    """Project detail page."""
    model = Projeto
    template_name = 'projetos/detalhe.html'
    context_object_name = 'projeto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Projeto.objects.filter(cliente=self.request.user)


class MensagensView(LoginRequiredMixin, DetailView):
    """Project messages view."""
    model = Projeto
    template_name = 'projetos/mensagens.html'
    context_object_name = 'projeto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Projeto.objects.filter(cliente=self.request.user)


class ArquivosView(LoginRequiredMixin, DetailView):
    """Project files view."""
    model = Projeto
    template_name = 'projetos/arquivos.html'
    context_object_name = 'projeto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Projeto.objects.filter(cliente=self.request.user)


class EnviarMensagemView(LoginRequiredMixin, View):
    """Send a message in a project."""

    def post(self, request, slug):
        projeto = get_object_or_404(Projeto, slug=slug, cliente=request.user)
        conteudo = request.POST.get('conteudo', '').strip()
        if conteudo:
            # Security (3.4): Sanitize message content before saving to prevent
            # stored XSS when the message is rendered in templates.
            conteudo = bleach.clean(
                conteudo,
                tags=_MSG_ALLOWED_TAGS,
                attributes=_MSG_ALLOWED_ATTRS,
                protocols=['http', 'https', 'mailto'],
                strip=True,
            )
            MensagemProjeto.objects.create(
                projeto=projeto,
                autor=request.user,
                conteudo=conteudo,
            )
        return redirect('projetos:mensagens', slug=slug)


class TimelineView(LoginRequiredMixin, DetailView):
    """Project timeline view."""
    model = Projeto
    template_name = 'projetos/timeline.html'
    context_object_name = 'projeto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Projeto.objects.filter(cliente=self.request.user)
