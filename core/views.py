"""Core app views."""
import logging

from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

from .models import Contato, FAQ, Depoimento
from servicos.models import Servico
from pacotes.models import Pacote
from portfolio.models import Case


class HomeView(TemplateView):
    """Homepage view."""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicos'] = Servico.objects.filter(ativo=True, destaque=True)[:4]
        context['pacotes'] = Pacote.objects.filter(ativo=True)[:3]
        context['cases'] = Case.objects.filter(ativo=True, destaque=True)[:6]
        context['depoimentos'] = Depoimento.objects.filter(ativo=True, destaque=True)[:3]
        return context


class SobreView(TemplateView):
    """About page view."""
    template_name = 'core/sobre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['depoimentos'] = Depoimento.objects.filter(ativo=True)[:6]
        return context


class ContatoView(CreateView):
    """Contact form view."""
    model = Contato
    template_name = 'core/contato.html'
    fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']
    success_url = reverse_lazy('core:contato')

    def form_valid(self, form):
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')
        response = super().form_valid(form)

        # Send email notification
        self.send_notification_email(self.object)

        messages.success(self.request, _('Mensagem enviada com sucesso! Entraremos em contato em breve.'))
        return response

    def send_notification_email(self, contato):
        """Send email notification for new contact message."""
        try:
            subject = f'Nova Mensagem de Contato: {contato.assunto}'

            message = f"""
Nova mensagem de contato recebida!

Nome: {contato.nome}
Email: {contato.email}
Telefone: {contato.telefone or 'Não informado'}

Assunto: {contato.assunto}

Mensagem:
{contato.mensagem}

---
ECOMMDEV - www.ecommdev.com.br
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ecommdev02@gmail.com'],
                fail_silently=True,
            )
        except Exception as e:
            logger.error("Error sending contact notification email: %s", e)

    def form_invalid(self, form):
        messages.error(self.request, _('Por favor, corrija os erros abaixo.'))
        return super().form_invalid(form)


class FAQView(TemplateView):
    """FAQ page view."""
    template_name = 'core/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(ativo=True)
        return context


class TermosView(TemplateView):
    """Terms of service page."""
    template_name = 'core/termos.html'


class PrivacidadeView(TemplateView):
    """Privacy policy page."""
    template_name = 'core/privacidade.html'


# =============================================================================
# CUSTOM ERROR HANDLERS
# =============================================================================

def error_400(request, exception=None):
    """400 Bad Request handler."""
    from django.shortcuts import render
    return render(request, '400.html', status=400)


def error_403(request, exception=None):
    """403 Forbidden handler."""
    from django.shortcuts import render
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    """404 Not Found handler."""
    from django.shortcuts import render
    return render(request, '404.html', status=404)


def error_500(request):
    """500 Internal Server Error handler."""
    from django.shortcuts import render
    return render(request, '500.html', status=500)
