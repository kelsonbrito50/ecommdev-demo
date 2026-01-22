"""Suporte app views."""
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, RespostaTicket, AvaliacaoTicket
from projetos.models import Projeto


class TicketListView(LoginRequiredMixin, ListView):
    """List all client tickets."""
    model = Ticket
    template_name = 'suporte/lista.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(cliente=self.request.user)


class TicketCreateView(LoginRequiredMixin, CreateView):
    """Create new ticket."""
    model = Ticket
    template_name = 'suporte/criar.html'
    fields = ['assunto', 'descricao', 'categoria', 'prioridade', 'projeto']

    def get_success_url(self):
        return reverse_lazy('suporte:detalhe', kwargs={'numero': self.object.numero})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['projeto'].queryset = Projeto.objects.filter(cliente=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.cliente = self.request.user
        messages.success(self.request, _('Ticket criado com sucesso!'))
        return super().form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    """Ticket detail page."""
    model = Ticket
    template_name = 'suporte/detalhe.html'
    context_object_name = 'ticket'
    slug_field = 'numero'
    slug_url_kwarg = 'numero'

    def get_queryset(self):
        return Ticket.objects.filter(cliente=self.request.user)


class TicketRespostaView(LoginRequiredMixin, View):
    """Add response to ticket."""

    def post(self, request, numero):
        ticket = get_object_or_404(Ticket, numero=numero, cliente=request.user)
        conteudo = request.POST.get('conteudo')
        if conteudo:
            RespostaTicket.objects.create(
                ticket=ticket,
                autor=request.user,
                conteudo=conteudo
            )
            messages.success(request, _('Resposta enviada!'))
        return redirect('suporte:detalhe', numero=numero)


class TicketAvaliacaoView(LoginRequiredMixin, View):
    """Rate ticket resolution."""

    def post(self, request, numero):
        ticket = get_object_or_404(Ticket, numero=numero, cliente=request.user)
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario', '')
        if nota:
            AvaliacaoTicket.objects.update_or_create(
                ticket=ticket,
                defaults={'nota': int(nota), 'comentario': comentario}
            )
            messages.success(request, _('Obrigado pela sua avaliação!'))
        return redirect('suporte:detalhe', numero=numero)
