"""Clientes app views."""
from django.views.generic import TemplateView, UpdateView, CreateView, View
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from .models import Usuario, PerfilEmpresa, SessaoAtiva
from .forms import RegistroForm, PerfilForm, AlterarSenhaForm
from core.ratelimit import RateLimitMixin


class LoginView(RateLimitMixin, BaseLoginView):
    """Custom login view with rate limiting."""
    template_name = 'clientes/login.html'
    redirect_authenticated_user = True
    ratelimit_key = 'login'
    ratelimit_rate = '5/m'
    ratelimit_block = 300  # 5 minutes


class RegistroView(RateLimitMixin, CreateView):
    """User registration view with rate limiting."""
    model = Usuario
    form_class = RegistroForm
    template_name = 'clientes/registro.html'
    success_url = reverse_lazy('clientes:verificar_email_enviado')
    ratelimit_key = 'register'
    ratelimit_rate = '3/m'
    ratelimit_block = 600  # 10 minutes

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        self.send_verification_email(user)
        messages.success(
            self.request,
            _('Conta criada! Verifique seu email para ativar sua conta.')
        )
        return response

    def send_verification_email(self, user):
        verification_url = self.request.build_absolute_uri(
            reverse('clientes:verificar_email', kwargs={'token': user.email_verification_token})
        )
        subject = _('Confirme seu email - ECOMMDEV')
        message = render_to_string('emails/verificar_email.html', {
            'user': user,
            'verification_url': verification_url,
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )


class PerfilView(LoginRequiredMixin, TemplateView):
    """User profile view."""
    template_name = 'clientes/perfil.html'


class PerfilEditarView(LoginRequiredMixin, UpdateView):
    """Edit user profile."""
    model = Usuario
    form_class = PerfilForm
    template_name = 'clientes/perfil_editar.html'
    success_url = reverse_lazy('clientes:perfil')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Perfil atualizado com sucesso!'))
        return super().form_valid(form)


class AlterarSenhaView(LoginRequiredMixin, TemplateView):
    """Change password view."""
    template_name = 'clientes/alterar_senha.html'

    def post(self, request, *args, **kwargs):
        form = AlterarSenhaForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Senha alterada com sucesso!'))
        return self.render_to_response({'form': form})


class SessoesView(LoginRequiredMixin, TemplateView):
    """Active sessions view."""
    template_name = 'clientes/sessoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessoes'] = SessaoAtiva.objects.filter(usuario=self.request.user)
        return context


class VerificarEmailView(View):
    """Email verification view."""

    def get(self, request, token):
        user = get_object_or_404(Usuario, email_verification_token=token)
        if not user.email_verified:
            user.email_verified = True
            user.is_active = True
            user.save(update_fields=['email_verified', 'is_active'])
            messages.success(request, _('Email verificado com sucesso! Agora você pode fazer login.'))
        else:
            messages.info(request, _('Este email já foi verificado.'))
        return redirect('clientes:login')


class VerificarEmailEnviadoView(TemplateView):
    """Email verification sent confirmation."""
    template_name = 'clientes/verificar_email_enviado.html'


class ReenviarVerificacaoView(RateLimitMixin, View):
    """Resend verification email with rate limiting."""
    ratelimit_key = 'resend_verification'
    ratelimit_rate = '3/h'
    ratelimit_block = 3600  # 1 hour

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = Usuario.objects.get(email=email, is_active=False)
            user.regenerate_verification_token()
            verification_url = request.build_absolute_uri(
                reverse('clientes:verificar_email', kwargs={'token': user.email_verification_token})
            )
            subject = _('Confirme seu email - ECOMMDEV')
            message = render_to_string('emails/verificar_email.html', {
                'user': user,
                'verification_url': verification_url,
            })
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=message,
                fail_silently=False,
            )
            messages.success(request, _('Email de verificação reenviado!'))
        except Usuario.DoesNotExist:
            messages.error(request, _('Email não encontrado ou conta já ativa.'))
        return redirect('clientes:verificar_email_enviado')
