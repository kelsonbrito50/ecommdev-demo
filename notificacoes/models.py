"""
Notificacoes App Models - Notifications system
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notificacao(models.Model):
    """User notification."""

    TIPO_CHOICES = [
        ("info", _("Informação")),
        ("sucesso", _("Sucesso")),
        ("aviso", _("Aviso")),
        ("erro", _("Erro")),
    ]

    CATEGORIA_CHOICES = [
        ("projeto", _("Projeto")),
        ("orcamento", _("Orçamento")),
        ("fatura", _("Fatura")),
        ("ticket", _("Ticket")),
        ("sistema", _("Sistema")),
        ("mensagem", _("Mensagem")),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        verbose_name=_("Usuário"),
    )
    tipo = models.CharField(_("Tipo"), max_length=20, choices=TIPO_CHOICES, default="info")
    categoria = models.CharField(
        _("Categoria"), max_length=20, choices=CATEGORIA_CHOICES, default="sistema"
    )
    titulo = models.CharField(_("Título"), max_length=200)
    mensagem = models.TextField(_("Mensagem"))
    url = models.CharField(_("URL"), max_length=255, blank=True)
    lida = models.BooleanField(_("Lida"), default=False)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Notificação")
        verbose_name_plural = _("Notificações")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"


class LogEmail(models.Model):
    """Email log."""

    STATUS_CHOICES = [
        ("enviado", _("Enviado")),
        ("falha", _("Falha")),
        ("pendente", _("Pendente")),
    ]

    TIPO_CHOICES = [
        ("orcamento_confirmacao", _("Confirmação de Orçamento")),
        ("orcamento_aprovado", _("Orçamento Aprovado")),
        ("projeto_atualizacao", _("Atualização de Projeto")),
        ("fatura_nova", _("Nova Fatura")),
        ("fatura_vencimento", _("Lembrete de Vencimento")),
        ("pagamento_confirmado", _("Pagamento Confirmado")),
        ("ticket_criado", _("Ticket Criado")),
        ("ticket_resposta", _("Resposta ao Ticket")),
        ("boas_vindas", _("Boas-vindas")),
        ("reset_senha", _("Reset de Senha")),
        ("newsletter", _("Newsletter")),
    ]

    destinatario = models.EmailField(_("Destinatário"))
    tipo = models.CharField(_("Tipo"), max_length=50, choices=TIPO_CHOICES)
    assunto = models.CharField(_("Assunto"), max_length=255)
    conteudo = models.TextField(_("Conteúdo"), blank=True)
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pendente"
    )
    erro = models.TextField(_("Erro"), blank=True)
    tentativas = models.PositiveSmallIntegerField(_("Tentativas"), default=0)
    enviado_at = models.DateTimeField(_("Enviado em"), null=True, blank=True)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Log de Email")
        verbose_name_plural = _("Logs de Email")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tipo} - {self.destinatario}"


class ConfiguracaoNotificacao(models.Model):
    """User notification preferences."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="config_notificacoes",
        verbose_name=_("Usuário"),
    )
    # Email notifications
    email_atualizacao_projeto = models.BooleanField(_("Atualizações de Projeto"), default=True)
    email_nova_fatura = models.BooleanField(_("Novas Faturas"), default=True)
    email_resposta_ticket = models.BooleanField(_("Respostas de Ticket"), default=True)
    email_newsletter = models.BooleanField(_("Newsletter"), default=False)
    email_marketing = models.BooleanField(_("Marketing"), default=False)

    # Push notifications
    push_atualizacao_projeto = models.BooleanField(_("Push - Atualizações"), default=True)
    push_nova_fatura = models.BooleanField(_("Push - Faturas"), default=True)
    push_resposta_ticket = models.BooleanField(_("Push - Tickets"), default=True)

    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Configuração de Notificação")
        verbose_name_plural = _("Configurações de Notificações")

    def __str__(self):
        return f"Config. Notificações - {self.usuario}"
