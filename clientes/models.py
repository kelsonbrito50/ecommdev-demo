"""
Clientes App Models - Custom User Model and Profile
"""
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import validate_avatar


class UsuarioManager(BaseUserManager):
    """Custom manager for Usuario model."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O email é obrigatório'))
        extra_fields.setdefault('is_active', False)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Custom User Model - Uses email instead of username."""

    username = None
    email = models.EmailField(_('Email'), unique=True)
    nome_completo = models.CharField(_('Nome Completo'), max_length=255)
    telefone = models.CharField(_('Telefone'), max_length=20, blank=True)
    cpf = models.CharField(_('CPF'), max_length=14, blank=True)
    foto = models.ImageField(
        _('Foto'),
        upload_to='usuarios/fotos/',
        blank=True,
        null=True,
        validators=[validate_avatar]
    )
    idioma_preferido = models.CharField(
        _('Idioma Preferido'),
        max_length=10,
        choices=[('pt-br', 'Português'), ('en', 'English')],
        default='pt-br'
    )
    notificacoes_email = models.BooleanField(_('Receber notificações por email'), default=True)
    notificacoes_sms = models.BooleanField(_('Receber notificações por SMS'), default=False)
    two_factor_enabled = models.BooleanField(_('2FA Ativado'), default=False)
    email_verified = models.BooleanField(_('Email Verificado'), default=False)
    email_verification_token = models.UUIDField(_('Token de Verificação'), default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    objects = UsuarioManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['-created_at']

    def __str__(self):
        return self.nome_completo or self.email

    def get_full_name(self):
        return self.nome_completo

    def get_short_name(self):
        return self.nome_completo.split()[0] if self.nome_completo else self.email

    def regenerate_verification_token(self):
        self.email_verification_token = uuid.uuid4()
        self.save(update_fields=['email_verification_token'])
        return self.email_verification_token


class PerfilEmpresa(models.Model):
    """Company profile for business clients."""

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='empresa',
        verbose_name=_('Usuário')
    )
    nome_empresa = models.CharField(_('Nome da Empresa'), max_length=255, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=18, blank=True)
    endereco = models.CharField(_('Endereço'), max_length=255, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True)
    estado = models.CharField(_('Estado'), max_length=2, blank=True)
    cep = models.CharField(_('CEP'), max_length=9, blank=True)
    website = models.URLField(_('Website'), blank=True)
    ramo_atividade = models.CharField(_('Ramo de Atividade'), max_length=100, blank=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = _('Perfil Empresa')
        verbose_name_plural = _('Perfis Empresa')

    def __str__(self):
        return self.nome_empresa or f"Empresa de {self.usuario}"


class LogLogin(models.Model):
    """Login history log."""

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='logs_login',
        verbose_name=_('Usuário')
    )
    ip_address = models.GenericIPAddressField(_('Endereço IP'))
    user_agent = models.TextField(_('User Agent'), blank=True)
    dispositivo = models.CharField(_('Dispositivo'), max_length=100, blank=True)
    localizacao = models.CharField(_('Localização'), max_length=100, blank=True)
    sucesso = models.BooleanField(_('Login bem sucedido'), default=True)
    created_at = models.DateTimeField(_('Data/Hora'), auto_now_add=True)

    class Meta:
        verbose_name = _('Log de Login')
        verbose_name_plural = _('Logs de Login')
        ordering = ['-created_at']

    def __str__(self):
        status = 'Sucesso' if self.sucesso else 'Falha'
        return f"{self.usuario} - {status} - {self.created_at}"


class SessaoAtiva(models.Model):
    """Active session tracking."""

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='sessoes_ativas',
        verbose_name=_('Usuário')
    )
    session_key = models.CharField(_('Chave da Sessão'), max_length=40)
    ip_address = models.GenericIPAddressField(_('Endereço IP'))
    dispositivo = models.CharField(_('Dispositivo'), max_length=100)
    navegador = models.CharField(_('Navegador'), max_length=100)
    ultimo_acesso = models.DateTimeField(_('Último Acesso'), auto_now=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Sessão Ativa')
        verbose_name_plural = _('Sessões Ativas')
        ordering = ['-ultimo_acesso']

    def __str__(self):
        return f"{self.usuario} - {self.dispositivo}"

    def is_current_session(self, request):
        """Check if this session matches the current request session."""
        return self.session_key == request.session.session_key
