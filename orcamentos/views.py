"""Orcamentos app views."""
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Orcamento
from pacotes.models import Pacote


class OrcamentoLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin that redirects to registro instead of login."""
    login_url = reverse_lazy('clientes:registro')

    def get_login_url(self):
        return str(self.login_url)


class OrcamentoCreateView(OrcamentoLoginRequiredMixin, CreateView):
    """Quote request form - requires login."""
    model = Orcamento
    template_name = 'orcamentos/criar.html'
    fields = [
        'nome_completo', 'email', 'telefone', 'empresa', 'cnpj',
        'cidade', 'estado', 'tipo_projeto', 'pacote', 'descricao_projeto',
        'objetivos', 'publico_alvo', 'orcamento_disponivel', 'prazo_desejado'
    ]
    success_url = reverse_lazy('orcamentos:sucesso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacotes'] = Pacote.objects.filter(ativo=True)
        return context

    def get_initial(self):
        """Pre-fill form with user data."""
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial['nome_completo'] = user.get_full_name() or user.email
            initial['email'] = user.email
            # Get phone from profile if exists
            if hasattr(user, 'telefone'):
                initial['telefone'] = user.telefone
        return initial

    def form_valid(self, form):
        from core.ratelimit import get_client_ip
        form.instance.ip_address = get_client_ip(self.request)
        # Always associate with logged-in user
        form.instance.cliente = self.request.user

        response = super().form_valid(form)

        # Send email notification to admin
        self.send_notification_email(self.object)

        messages.success(self.request, _('Orçamento enviado com sucesso!'))
        return response

    def send_notification_email(self, orcamento):
        """Send email notification for new quote request."""
        import logging
        logger = logging.getLogger(__name__)

        subject = f'Novo Orçamento: {orcamento.numero} - {orcamento.nome_completo}'

        message = f"""
Novo orçamento recebido!

Número: {orcamento.numero}
Nome: {orcamento.nome_completo}
Email: {orcamento.email}
Telefone: {orcamento.telefone}
Empresa: {orcamento.empresa or 'Não informada'}

Tipo de Projeto: {orcamento.get_tipo_projeto_display()}
Pacote: {orcamento.pacote.nome if orcamento.pacote else 'Não selecionado'}

Descrição:
{orcamento.descricao_projeto}

Orçamento Disponível: {orcamento.orcamento_disponivel or 'Não informado'}
Prazo Desejado: {orcamento.prazo_desejado or 'Não informado'}

---
Acesse o painel admin para mais detalhes.
        """

        try:
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ecommdev02@gmail.com'],
                fail_silently=False,
            )
            logger.info(f"Email sent for orcamento {orcamento.numero}: result={result}")
        except Exception as e:
            logger.error(f"Error sending email for orcamento {orcamento.numero}: {e}")


class OrcamentoSucessoView(TemplateView):
    """Quote success page."""
    template_name = 'orcamentos/sucesso.html'


class MeusOrcamentosView(LoginRequiredMixin, ListView):
    """List user's quote requests."""
    model = Orcamento
    template_name = 'orcamentos/meus_orcamentos.html'
    context_object_name = 'orcamentos'

    def get_queryset(self):
        return Orcamento.objects.filter(cliente=self.request.user)
