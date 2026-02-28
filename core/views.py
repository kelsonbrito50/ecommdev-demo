"""Core app views."""

import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView

from pacotes.models import Pacote
from portfolio.models import Case
from servicos.models import Servico

from .models import FAQ, Contato, Depoimento

logger = logging.getLogger(__name__)

# =============================================================================
# HONEYPOT MIXIN — bot protection for public forms
# =============================================================================


class HoneypotMixin:
    """
    Mixin that silently discards form submissions where the honeypot field is filled.

    How it works:
      - A hidden input field (name="website") is added to the form template
        via style="display:none" so real users never see or fill it.
      - Bots that blindly fill all inputs will populate this field.
      - If the field is non-empty on POST, we redirect to the success URL
        without saving anything, giving bots no useful error feedback.

    Template usage (add inside the <form> tag):
        <div style="display:none!important; position:absolute; left:-9999px;" aria-hidden="true">
            <input type="text" name="website" tabindex="-1" autocomplete="off"
                   placeholder="Leave this empty">
        </div>
    """

    honeypot_field = "website"  # Must match the hidden input name in templates

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            honeypot_value = request.POST.get(self.honeypot_field, "").strip()
            if honeypot_value:
                # Bot detected — silently redirect without saving
                logger.warning(
                    "Honeypot triggered on %s from IP %s",
                    request.path,
                    request.META.get("REMOTE_ADDR", "unknown"),
                )
                return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    """Homepage view."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["servicos"] = Servico.objects.filter(ativo=True, destaque=True)[:4]
        context["pacotes"] = Pacote.objects.filter(ativo=True).order_by("ordem")
        context["cases"] = Case.objects.filter(ativo=True, destaque=True)[:6]
        context["depoimentos"] = Depoimento.objects.filter(ativo=True, destaque=True)[:3]
        return context


class SobreView(TemplateView):
    """About page view."""

    template_name = "core/sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["depoimentos"] = Depoimento.objects.filter(ativo=True)[:6]
        return context


class ContatoView(HoneypotMixin, CreateView):
    """Contact form view — HoneypotMixin silently drops bot submissions."""

    model = Contato
    template_name = "core/contato.html"
    fields = ["nome", "email", "telefone", "assunto", "mensagem"]
    success_url = reverse_lazy("core:contato")

    def form_valid(self, form):
        form.instance.ip_address = self.request.META.get("REMOTE_ADDR")
        response = super().form_valid(form)

        # Send email notification
        self.send_notification_email(self.object)

        messages.success(
            self.request, _("Mensagem enviada com sucesso! Entraremos em contato em breve.")
        )
        return response

    def send_notification_email(self, contato):
        """Send email notification for new contact message."""
        try:
            subject = f"Nova Mensagem de Contato: {contato.assunto}"

            message = f"""
Nova mensagem de contato recebida!

Nome: {contato.nome}
Email: {contato.email}
Telefone: {contato.telefone or "Não informado"}

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
                recipient_list=["contato@ecommdev.com.br"],
                fail_silently=True,
            )
        except Exception as e:
            logger.error("Error sending contact notification email: %s", e)

    def form_invalid(self, form):
        messages.error(self.request, _("Por favor, corrija os erros abaixo."))
        return super().form_invalid(form)


class FAQView(TemplateView):
    """FAQ page view."""

    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FAQ.objects.filter(ativo=True)
        return context


class TermosView(TemplateView):
    """Terms of service page."""

    template_name = "core/termos.html"


class PrivacidadeView(TemplateView):
    """Privacy policy page."""

    template_name = "core/privacidade.html"


# =============================================================================
# CUSTOM ERROR HANDLERS
# =============================================================================


def error_400(request, exception=None):
    """400 Bad Request handler."""
    from django.shortcuts import render

    return render(request, "400.html", status=400)


def error_403(request, exception=None):
    """403 Forbidden handler."""
    from django.shortcuts import render

    return render(request, "403.html", status=403)


def error_404(request, exception=None):
    """404 Not Found handler."""
    from django.shortcuts import render

    return render(request, "404.html", status=404)


def error_500(request):
    """500 Internal Server Error handler."""
    from django.shortcuts import render

    return render(request, "500.html", status=500)
