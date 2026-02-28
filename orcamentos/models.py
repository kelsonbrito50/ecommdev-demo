"""
Orcamentos App Models - Quote requests
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Orcamento(models.Model):
    """Quote request from potential clients."""

    STATUS_CHOICES = [
        ("novo", _("Novo")),
        ("em_analise", _("Em Análise")),
        ("aguardando_info", _("Aguardando Informações")),
        ("proposta_enviada", _("Proposta Enviada")),
        ("aprovado", _("Aprovado")),
        ("rejeitado", _("Rejeitado")),
        ("cancelado", _("Cancelado")),
    ]

    TIPO_PROJETO_CHOICES = [
        ("ecommerce", _("E-commerce")),
        ("corporativo", _("Site Corporativo")),
        ("personalizado", _("Solução Personalizada")),
        ("manutencao", _("Manutenção")),
    ]

    # Auto-generated number
    numero = models.CharField(_("Número"), max_length=20, unique=True, blank=True)

    # Client info
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orcamentos",
        verbose_name=_("Cliente"),
    )
    nome_completo = models.CharField(_("Nome Completo"), max_length=255)
    email = models.EmailField(_("Email"))
    telefone = models.CharField(_("Telefone/WhatsApp"), max_length=20)
    empresa = models.CharField(_("Empresa"), max_length=200, blank=True)
    cnpj = models.CharField(_("CNPJ"), max_length=18, blank=True)
    cidade = models.CharField(_("Cidade"), max_length=100)
    estado = models.CharField(_("Estado"), max_length=2)

    # Project info
    tipo_projeto = models.CharField(
        _("Tipo de Projeto"), max_length=20, choices=TIPO_PROJETO_CHOICES
    )
    pacote = models.ForeignKey(
        "pacotes.Pacote",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orcamentos",
        verbose_name=_("Pacote de Interesse"),
    )
    descricao_projeto = models.TextField(_("Descrição do Projeto"))
    objetivos = models.TextField(_("Objetivos do Negócio"), blank=True)
    publico_alvo = models.TextField(_("Público-Alvo"), blank=True)

    # Technical requirements
    funcionalidades = models.JSONField(_("Funcionalidades Necessárias"), default=list, blank=True)
    integracoes = models.JSONField(_("Integrações Necessárias"), default=list, blank=True)
    sistema_pagamento = models.CharField(_("Sistema de Pagamento"), max_length=100, blank=True)
    referencia_design = models.TextField(_("Referência de Design/Layout"), blank=True)
    possui_dominio = models.BooleanField(_("Já possui domínio?"), default=False)
    possui_hospedagem = models.BooleanField(_("Já possui hospedagem?"), default=False)

    # Budget and timeline
    orcamento_disponivel = models.CharField(_("Orçamento Disponível"), max_length=100, blank=True)
    prazo_desejado = models.CharField(_("Prazo Desejado"), max_length=100, blank=True)
    data_inicio_preferida = models.DateField(_("Data de Início Preferida"), null=True, blank=True)

    # Attachments
    anexos = models.JSONField(_("Anexos"), default=list, blank=True)

    # Status and tracking
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="novo")
    observacoes_internas = models.TextField(_("Observações Internas"), blank=True)
    valor_proposto = models.DecimalField(
        _("Valor Proposto"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Metadata
    ip_address = models.GenericIPAddressField(_("IP"), blank=True, null=True)
    origem = models.CharField(_("Origem"), max_length=100, blank=True)
    created_at = models.DateTimeField(_("Solicitado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Orçamento")
        verbose_name_plural = _("Orçamentos")
        ordering = ["-created_at"]

    # Valid status transitions: current_status -> set of allowed next statuses
    VALID_TRANSITIONS = {
        "novo": {"em_analise", "cancelado"},
        "em_analise": {"aguardando_info", "proposta_enviada", "cancelado"},
        "aguardando_info": {"em_analise", "cancelado"},
        "proposta_enviada": {"aprovado", "rejeitado", "cancelado"},
        "aprovado": set(),
        "rejeitado": set(),
        "cancelado": set(),
    }

    def clean(self):
        """Enforce valid state-machine transitions on Orcamento status."""
        super().clean()
        if not self.pk:
            # New instance — allow any initial status (defaults to 'novo')
            return
        try:
            original = Orcamento.objects.get(pk=self.pk)
        except Orcamento.DoesNotExist:
            return
        if original.status == self.status:
            return  # No change — always valid
        allowed = self.VALID_TRANSITIONS.get(original.status, set())
        if self.status not in allowed:
            raise ValidationError(
                _(
                    'Transição de status inválida: "%(from)s" → "%(to)s". '
                    "Transições permitidas: %(allowed)s"
                ),
                params={
                    "from": original.status,
                    "to": self.status,
                    "allowed": ", ".join(sorted(allowed)) if allowed else _("nenhuma"),
                },
            )

    def __str__(self):
        return f"{self.numero} - {self.nome_completo}"

    def save(self, *args, **kwargs):
        if not self.numero:
            from datetime import datetime

            from django.db.models import Max

            year = datetime.now().year
            prefix = f"ORC-{year}-"
            last = Orcamento.objects.filter(numero__startswith=prefix).aggregate(
                max_num=Max("numero")
            )["max_num"]
            if last:
                count = int(last.split("-")[-1]) + 1
            else:
                count = 1
            self.numero = f"{prefix}{count:04d}"
        super().save(*args, **kwargs)


class HistoricoOrcamento(models.Model):
    """History/timeline of quote changes."""

    orcamento = models.ForeignKey(
        Orcamento, on_delete=models.CASCADE, related_name="historico", verbose_name=_("Orçamento")
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Usuário"),
    )
    acao = models.CharField(_("Ação"), max_length=100)
    status_anterior = models.CharField(_("Status Anterior"), max_length=20, blank=True)
    status_novo = models.CharField(_("Novo Status"), max_length=20, blank=True)
    observacao = models.TextField(_("Observação"), blank=True)
    created_at = models.DateTimeField(_("Data/Hora"), auto_now_add=True)

    class Meta:
        verbose_name = _("Histórico do Orçamento")
        verbose_name_plural = _("Históricos de Orçamentos")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.orcamento.numero} - {self.acao}"
