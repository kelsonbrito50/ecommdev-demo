"""
Pacotes App Models - Pricing packages
"""

from decimal import Decimal

from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class Pacote(models.Model):
    """Pricing package."""

    TIPO_CHOICES = [
        ("basico", _("Básico")),
        ("completo", _("Completo")),
        ("premium", _("Premium")),
        ("personalizado", _("Personalizado")),
    ]

    tipo = models.CharField(_("Tipo"), max_length=20, choices=TIPO_CHOICES, unique=True)
    nome_pt = models.CharField(_("Nome (PT)"), max_length=100)
    nome_en = models.CharField(_("Nome (EN)"), max_length=100, blank=True)
    subtitulo_pt = models.CharField(_("Subtítulo (PT)"), max_length=200, blank=True)
    subtitulo_en = models.CharField(_("Subtítulo (EN)"), max_length=200, blank=True)
    descricao_pt = models.TextField(_("Descrição (PT)"), blank=True)
    descricao_en = models.TextField(_("Descrição (EN)"), blank=True)
    preco = models.DecimalField(
        _("Preço"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    preco_promocional = models.DecimalField(
        _("Preço Promocional"), max_digits=10, decimal_places=2, blank=True, null=True
    )

    # Package details
    tempo_desenvolvimento = models.CharField(
        _("Tempo de Desenvolvimento"), max_length=50, blank=True
    )
    suporte_dias = models.PositiveIntegerField(_("Dias de Suporte"), default=30)
    horas_treinamento = models.PositiveIntegerField(_("Horas de Treinamento"), default=0)

    # Display
    destaque = models.BooleanField(_("Destacar (Mais Popular)"), default=False)
    cor_destaque = models.CharField(_("Cor de Destaque"), max_length=20, default="#0066CC")
    icone = models.CharField(_("Ícone"), max_length=50, blank=True)
    ativo = models.BooleanField(_("Ativo"), default=True)
    ordem = models.PositiveIntegerField(_("Ordem de Exibição"), default=0)

    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Pacote")
        verbose_name_plural = _("Pacotes")
        ordering = ["ordem", "preco"]

    def __str__(self):
        return f"{self.nome_pt} - R$ {self.preco:,.2f}"

    @property
    def nome(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.nome_en:
            return self.nome_en
        return self.nome_pt

    @property
    def subtitulo(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.subtitulo_en:
            return self.subtitulo_en
        return self.subtitulo_pt

    @property
    def descricao(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.descricao_en:
            return self.descricao_en
        return self.descricao_pt

    def get_preco_final(self):
        return self.preco_promocional or self.preco


class RecursoPacote(models.Model):
    """Features included in a package."""

    pacote = models.ForeignKey(
        Pacote, on_delete=models.CASCADE, related_name="recursos", verbose_name=_("Pacote")
    )
    titulo_pt = models.CharField(_("Recurso (PT)"), max_length=200)
    titulo_en = models.CharField(_("Recurso (EN)"), max_length=200, blank=True)
    incluido = models.BooleanField(_("Incluído"), default=True)
    destaque = models.BooleanField(_("Destaque"), default=False)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)

    class Meta:
        verbose_name = _("Recurso do Pacote")
        verbose_name_plural = _("Recursos do Pacote")
        ordering = ["ordem"]

    @property
    def titulo(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.titulo_en:
            return self.titulo_en
        return self.titulo_pt

    def __str__(self):
        status = "✓" if self.incluido else "✗"
        return f"{self.pacote.nome_pt} - {status} {self.titulo_pt}"


class Adicional(models.Model):
    """Add-ons that can be purchased with any package."""

    nome_pt = models.CharField(_("Nome (PT)"), max_length=100)
    nome_en = models.CharField(_("Nome (EN)"), max_length=100, blank=True)
    descricao_pt = models.TextField(_("Descrição (PT)"), blank=True)
    descricao_en = models.TextField(_("Descrição (EN)"), blank=True)
    preco = models.DecimalField(_("Preço"), max_digits=10, decimal_places=2)
    tipo_cobranca = models.CharField(
        _("Tipo de Cobrança"),
        max_length=20,
        choices=[
            ("unico", _("Único")),
            ("mensal", _("Mensal")),
            ("hora", _("Por Hora")),
        ],
        default="unico",
    )
    ativo = models.BooleanField(_("Ativo"), default=True)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)

    class Meta:
        verbose_name = _("Adicional")
        verbose_name_plural = _("Adicionais")
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.nome_pt} - R$ {self.preco:,.2f}"
