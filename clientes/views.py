"""Clientes app views."""
import logging
from urllib.parse import urlparse

from django.views.generic import TemplateView, UpdateView, CreateView, View
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from .models import Usuario, PerfilEmpresa, SessaoAtiva, LogLogin
from .forms import RegistroForm, PerfilForm, AlterarSenhaForm
from core.ratelimit import RateLimitMixin, get_client_ip

logger = logging.getLogger(__name__)


class LoginView(RateLimitMixin, BaseLoginView):
    """
    Custom login view with rate limiting and account lockout.

    Security features:
    - IP-based rate limiting (5 attempts/minute)
    - Account-based lockout (10 failed attempts = 30 min lockout)
    - Login attempt logging
    - Safe redirect validation
    """
    template_name = 'clientes/login.html'
    redirect_authenticated_user = True
    ratelimit_key = 'login'
    ratelimit_rate = '5/m'
    ratelimit_block = 300  # 5 minutes

    # Account lockout settings
    MAX_FAILED_ATTEMPTS = 10
    LOCKOUT_DURATION = 1800  # 30 minutes

    def form_valid(self, form):
        """Handle successful login."""
        user = form.get_user()

        # Clear failed attempt counter on successful login
        cache_key = f'login_failures:{user.email}'
        cache.delete(cache_key)

        # Log successful login
        self._log_login_attempt(user, success=True)

        # Regenerate session to prevent fixation
        try:
            if hasattr(self.request, 'session'):
                self.request.session.cycle_key()
        except Exception as e:
            logger.warning(f"Session cycle error on login: {e}")

        logger.info(f"Successful login for user {user.id} from {get_client_ip(self.request)}")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle failed login attempt."""
        email = form.data.get('username', '')  # Django uses 'username' field

        # Try to find the user to log the attempt
        try:
            user = Usuario.objects.get(email=email)
            self._log_login_attempt(user, success=False)
            self._increment_failed_attempts(email)
        except Usuario.DoesNotExist:
            # Don't reveal that user doesn't exist
            pass

        logger.warning(f"Failed login attempt for {email} from {get_client_ip(self.request)}")

        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """Check for account lockout before processing."""
        if request.method == 'POST':
            email = request.POST.get('username', '')
            if self._is_account_locked(email):
                messages.error(
                    request,
                    _('Conta temporariamente bloqueada devido a muitas tentativas. Tente novamente em 30 minutos.')
                )
                return self.render_to_response(self.get_context_data())

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Validate redirect URL to prevent open redirect."""
        redirect_to = self.request.GET.get('next', '') or self.request.POST.get('next', '')

        # SECURITY: Validate redirect URL is safe
        if redirect_to:
            parsed = urlparse(redirect_to)
            # Only allow relative URLs or URLs to our own domain
            if parsed.netloc and parsed.netloc not in settings.ALLOWED_HOSTS:
                logger.warning(f"Blocked open redirect attempt to {redirect_to}")
                redirect_to = ''

        return redirect_to or settings.LOGIN_REDIRECT_URL

    def _is_account_locked(self, email):
        """Check if account is locked due to too many failed attempts."""
        if not email:
            return False
        cache_key = f'login_failures:{email}'
        failures = cache.get(cache_key, 0)
        return failures >= self.MAX_FAILED_ATTEMPTS

    def _increment_failed_attempts(self, email):
        """Increment failed login counter for account."""
        if not email:
            return
        cache_key = f'login_failures:{email}'
        failures = cache.get(cache_key, 0)
        cache.set(cache_key, failures + 1, self.LOCKOUT_DURATION)

    def _log_login_attempt(self, user, success):
        """Log login attempt for security auditing."""
        try:
            LogLogin.objects.create(
                usuario=user,
                ip_address=get_client_ip(self.request),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')[:500],
                sucesso=success
            )
        except Exception as e:
            logger.error(f"Failed to log login attempt: {e}")


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
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=message,
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {e}")
            # Re-raise to show error to user in development
            if settings.DEBUG:
                raise


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = AlterarSenhaForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = AlterarSenhaForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # SECURITY: Regenerate session after password change
            request.session.cycle_key()
            messages.success(request, _('Senha alterada com sucesso!'))
            logger.info(f"Password changed for user {user.id}")
            return redirect('clientes:perfil')
        else:
            # Show form errors
            messages.error(request, _('Por favor, corrija os erros abaixo.'))
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
        # SECURITY: Use generic message to prevent user enumeration.
        # Always show the same message regardless of whether the email exists.
        generic_message = _('Se este email estiver cadastrado e ainda não verificado, você receberá um link de verificação.')

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
                fail_silently=True,  # Don't reveal errors to user
            )
        except Usuario.DoesNotExist:
            # SECURITY: Don't reveal that email doesn't exist
            pass

        # Always show the same message to prevent enumeration
        messages.info(request, generic_message)
        return redirect('clientes:verificar_email_enviado')
