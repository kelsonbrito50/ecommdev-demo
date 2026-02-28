"""
Faturas App Models - Invoicing and payments
"""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Fatura(models.Model):
    """Invoice."""

    STATUS_CHOICES = [
        ("rascunho", _("Rascunho")),
        ("pendente", _("Pendente")),
        ("paga", _("Paga")),
        ("vencida", _("Vencida")),
        ("cancelada", _("Cancelada")),
        ("reembolsada", _("Reembolsada")),
    ]

    # Auto-generated number
    numero = models.CharField(_("Número"), max_length=20, unique=True, blank=True)

    # References
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="faturas",
        verbose_name=_("Cliente"),
    )
    projeto = models.ForeignKey(
        "projetos.Projeto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faturas",
        verbose_name=_("Projeto"),
    )

    # Invoice details
    descricao = models.TextField(_("Descrição"), blank=True)
    subtotal = models.DecimalField(
        _("Subtotal"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    desconto = models.DecimalField(
        _("Desconto"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    impostos = models.DecimalField(
        _("Impostos"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    valor_total = models.DecimalField(
        _("Valor Total"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # Dates
    data_emissao = models.DateField(_("Data de Emissão"), auto_now_add=True)
    data_vencimento = models.DateField(_("Data de Vencimento"))
    data_pagamento = models.DateField(_("Data de Pagamento"), null=True, blank=True)

    # Status
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pendente"
    )
    observacoes = models.TextField(_("Observações"), blank=True)
    observacoes_internas = models.TextField(_("Observações Internas"), blank=True)

    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Fatura")
        verbose_name_plural = _("Faturas")
        ordering = ["-created_at"]

    # Valid status transitions: current_status -> set of allowed next statuses
    VALID_TRANSITIONS = {
        "rascunho": {"pendente", "cancelada"},
        "pendente": {"paga", "vencida", "cancelada"},
        "vencida": {"paga", "cancelada"},
        "paga": {"reembolsada"},
        "cancelada": set(),
        "reembolsada": set(),
    }

    def clean(self):
        """Enforce valid state-machine transitions on Fatura status."""
        super().clean()
        if not self.pk:
            # New instance — allow any initial status (defaults to 'pendente')
            return
        try:
            original = Fatura.objects.get(pk=self.pk)
        except Fatura.DoesNotExist:
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

    @property
    def status_color(self):
        colors = {
            "rascunho": "secondary",
            "pendente": "warning",
            "paga": "success",
            "vencida": "danger",
            "cancelada": "secondary",
            "reembolsada": "info",
        }
        return colors.get(self.status, "secondary")

    def __str__(self):
        return f"{self.numero} - R$ {self.valor_total:,.2f}"

    def save(self, *args, **kwargs):
        if not self.numero:
            from datetime import datetime

            from django.db.models import Max

            year = datetime.now().year
            prefix = f"INV-{year}-"
            last = Fatura.objects.filter(numero__startswith=prefix).aggregate(
                max_num=Max("numero")
            )["max_num"]
            if last:
                count = int(last.split("-")[-1]) + 1
            else:
                count = 1
            self.numero = f"{prefix}{count:04d}"
        # Calculate total
        self.valor_total = self.subtotal - self.desconto + self.impostos
        super().save(*args, **kwargs)

    def calcular_total(self):
        """Recalculate from items."""
        self.subtotal = sum(item.subtotal for item in self.itens.all())
        self.valor_total = self.subtotal - self.desconto + self.impostos
        self.save()


class ItemFatura(models.Model):
    """Invoice line item."""

    fatura = models.ForeignKey(
        Fatura, on_delete=models.CASCADE, related_name="itens", verbose_name=_("Fatura")
    )
    descricao = models.CharField(_("Descrição"), max_length=255)
    quantidade = models.PositiveIntegerField(_("Quantidade"), default=1)
    valor_unitario = models.DecimalField(_("Valor Unitário"), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_("Subtotal"), max_digits=10, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _("Item da Fatura")
        verbose_name_plural = _("Itens da Fatura")

    def __str__(self):
        return f"{self.descricao} - R$ {self.subtotal:,.2f}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)


class Pagamento(models.Model):
    """Payment record."""

    METODO_CHOICES = [
        ("pix", _("PIX")),
        ("boleto", _("Boleto Bancário")),
        ("cartao_credito", _("Cartão de Crédito")),
        ("cartao_debito", _("Cartão de Débito")),
        ("transferencia", _("Transferência Bancária")),
    ]

    STATUS_CHOICES = [
        ("pendente", _("Pendente")),
        ("processando", _("Processando")),
        ("aprovado", _("Aprovado")),
        ("recusado", _("Recusado")),
        ("cancelado", _("Cancelado")),
        ("reembolsado", _("Reembolsado")),
    ]

    fatura = models.ForeignKey(
        Fatura, on_delete=models.PROTECT, related_name="pagamentos", verbose_name=_("Fatura")
    )
    metodo = models.CharField(_("Método"), max_length=20, choices=METODO_CHOICES)
    valor = models.DecimalField(_("Valor"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="pendente"
    )

    # Payment gateway info
    transacao_id = models.CharField(_("ID da Transação"), max_length=100, blank=True)
    gateway = models.CharField(_("Gateway"), max_length=50, default="mercadopago")
    dados_gateway = models.JSONField(_("Dados do Gateway"), default=dict, blank=True)

    # Dates
    data_pagamento = models.DateTimeField(_("Data do Pagamento"), null=True, blank=True)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Pagamento")
        verbose_name_plural = _("Pagamentos")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.fatura.numero} - {self.metodo} - R$ {self.valor:,.2f}"
