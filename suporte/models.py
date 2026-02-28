"""
Suporte App Models - Support tickets
"""
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Ticket(models.Model):
    """Support ticket."""

    STATUS_CHOICES = [
        ('aberto', _('Aberto')),
        ('em_atendimento', _('Em Atendimento')),
        ('aguardando_cliente', _('Aguardando Cliente')),
        ('resolvido', _('Resolvido')),
        ('fechado', _('Fechado')),
    ]

    PRIORIDADE_CHOICES = [
        ('baixa', _('Baixa')),
        ('media', _('Média')),
        ('alta', _('Alta')),
        ('urgente', _('Urgente')),
    ]

    CATEGORIA_CHOICES = [
        ('tecnico', _('Técnico - Bug')),
        ('duvida', _('Dúvida - Como Fazer')),
        ('solicitacao', _('Solicitação - Nova Feature')),
        ('financeiro', _('Financeiro - Fatura')),
        ('outro', _('Outro')),
    ]

    # Auto-generated number
    numero = models.CharField(_('Número'), max_length=20, unique=True, blank=True)

    # References
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tickets',
        verbose_name=_('Cliente')
    )
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name=_('Projeto Relacionado')
    )
    atendente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_atendimento',
        verbose_name=_('Atendente')
    )

    # Ticket info
    assunto = models.CharField(_('Assunto'), max_length=200)
    descricao = models.TextField(_('Descrição'))
    categoria = models.CharField(_('Categoria'), max_length=20, choices=CATEGORIA_CHOICES)
    prioridade = models.CharField(_('Prioridade'), max_length=20, choices=PRIORIDADE_CHOICES, default='media')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='aberto')

    # Attachments
    anexos = models.JSONField(_('Anexos'), default=list, blank=True)

    # Tracking
    data_primeira_resposta = models.DateTimeField(_('Primeira Resposta'), null=True, blank=True)
    data_resolucao = models.DateTimeField(_('Data de Resolução'), null=True, blank=True)

    created_at = models.DateTimeField(_('Aberto em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero} - {self.assunto}"

    def save(self, *args, **kwargs):
        if not self.numero:
            from datetime import datetime
            from django.db.models import Max
            year = datetime.now().year
            prefix = f"TKT-{year}-"
            last = Ticket.objects.filter(
                numero__startswith=prefix
            ).aggregate(max_num=Max('numero'))['max_num']
            if last:
                count = int(last.split('-')[-1]) + 1
            else:
                count = 1
            self.numero = f"{prefix}{count:04d}"
        super().save(*args, **kwargs)


class RespostaTicket(models.Model):
    """Ticket response/reply."""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name=_('Ticket')
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Autor')
    )
    conteudo = models.TextField(
        _('Resposta'),
        validators=[MaxLengthValidator(10000, _('Resposta não pode exceder 10.000 caracteres.'))],
    )
    solucao_proposta = models.TextField(_('Solução Proposta'), blank=True)
    anexos = models.JSONField(_('Anexos'), default=list, blank=True)
    interno = models.BooleanField(_('Nota Interna'), default=False)
    created_at = models.DateTimeField(_('Enviado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Resposta do Ticket')
        verbose_name_plural = _('Respostas do Ticket')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.ticket.numero} - Resposta de {self.autor}"


class AvaliacaoTicket(models.Model):
    """Ticket satisfaction rating."""

    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='avaliacao',
        verbose_name=_('Ticket')
    )
    nota = models.PositiveSmallIntegerField(
        _('Nota'),
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comentario = models.TextField(_('Comentário'), blank=True)
    created_at = models.DateTimeField(_('Avaliado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Avaliação do Ticket')
        verbose_name_plural = _('Avaliações de Tickets')

    def __str__(self):
        return f"{self.ticket.numero} - {self.nota} estrelas"
