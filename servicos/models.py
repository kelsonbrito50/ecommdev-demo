"""
Servicos App Models - Service catalog
"""

from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from core.validators import validate_image


class Servico(models.Model):
    """Service offered by the agency."""

    TIPO_CHOICES = [
        ("desenvolvimento", _("Desenvolvimento Web")),
        ("ecommerce", _("E-commerce")),
        ("landing", _("Landing Page")),
        ("sistema", _("Sistema Personalizado")),
        ("manutencao", _("Manutenção e Suporte")),
        ("design", _("Design e Identidade Visual")),
        ("marketing", _("Marketing Digital")),
        ("integracao", _("Integrações e Automações")),
        ("treinamento", _("Treinamento e Consultoria")),
        ("pacote", _("Pacote Promocional")),
    ]

    tipo = models.CharField(_("Tipo"), max_length=20, choices=TIPO_CHOICES)
    nome_pt = models.CharField(_("Nome (PT)"), max_length=100)
    nome_en = models.CharField(_("Nome (EN)"), max_length=100, blank=True)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    descricao_curta_pt = models.CharField(_("Descrição Curta (PT)"), max_length=255)
    descricao_curta_en = models.CharField(_("Descrição Curta (EN)"), max_length=255, blank=True)
    descricao_pt = models.TextField(_("Descrição Completa (PT)"))
    descricao_en = models.TextField(_("Descrição Completa (EN)"), blank=True)
    icone = models.CharField(_("Ícone (CSS class)"), max_length=50, blank=True)
    imagem = models.ImageField(
        _("Imagem"), upload_to="servicos/", blank=True, null=True, validators=[validate_image]
    )

    # Pricing
    preco = models.DecimalField(
        _("Preço"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    preco_ate = models.DecimalField(
        _("Preço Até"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    tipo_preco = models.CharField(
        _("Tipo de Preço"),
        max_length=20,
        choices=[
            ("fixo", _("Preço Fixo")),
            ("apartir", _("A partir de")),
            ("mensal", _("Mensal")),
            ("hora", _("Por Hora")),
        ],
        default="apartir",
    )
    prazo = models.CharField(_("Prazo de Entrega"), max_length=100, blank=True)
    ideal_para = models.TextField(_("Ideal Para"), blank=True)

    # Technical details
    tecnologias = models.JSONField(_("Tecnologias"), default=list, blank=True)
    beneficios_pt = models.JSONField(_("Benefícios/Incluído (PT)"), default=list, blank=True)
    beneficios_en = models.JSONField(_("Benefícios/Incluído (EN)"), default=list, blank=True)

    ativo = models.BooleanField(_("Ativo"), default=True)
    destaque = models.BooleanField(_("Destaque na Home"), default=False)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Serviço")
        verbose_name_plural = _("Serviços")
        ordering = ["ordem", "nome_pt"]

    def __str__(self):
        return self.nome_pt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome_pt)
        super().save(*args, **kwargs)

    @property
    def nome(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.nome_en:
            return self.nome_en
        return self.nome_pt

    @property
    def descricao_curta(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.descricao_curta_en:
            return self.descricao_curta_en
        return self.descricao_curta_pt

    @property
    def descricao(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.descricao_en:
            return self.descricao_en
        return self.descricao_pt

    @property
    def beneficios(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.beneficios_en:
            return self.beneficios_en
        return self.beneficios_pt

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("servicos:detalhe", kwargs={"slug": self.slug})

    def get_preco_display(self):
        if self.tipo_preco == "apartir":
            return (
                f"A partir de R$ {self.preco:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
        elif self.tipo_preco == "mensal":
            return f"R$ {self.preco:,.2f}/mês".replace(",", "X").replace(".", ",").replace("X", ".")
        elif self.tipo_preco == "hora":
            return (
                f"R$ {self.preco:,.2f}/hora".replace(",", "X").replace(".", ",").replace("X", ".")
            )
        else:
            return f"R$ {self.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class RecursoServico(models.Model):
    """Features/resources of a service."""

    servico = models.ForeignKey(
        Servico, on_delete=models.CASCADE, related_name="recursos", verbose_name=_("Serviço")
    )
    titulo_pt = models.CharField(_("Título (PT)"), max_length=100)
    titulo_en = models.CharField(_("Título (EN)"), max_length=100, blank=True)
    descricao_pt = models.TextField(_("Descrição (PT)"), blank=True)
    descricao_en = models.TextField(_("Descrição (EN)"), blank=True)
    icone = models.CharField(_("Ícone"), max_length=50, blank=True)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)

    class Meta:
        verbose_name = _("Recurso do Serviço")
        verbose_name_plural = _("Recursos do Serviço")
        ordering = ["ordem"]

    @property
    def titulo(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.titulo_en:
            return self.titulo_en
        return self.titulo_pt

    @property
    def descricao(self):
        lang = get_language()
        if lang and lang.startswith("en") and self.descricao_en:
            return self.descricao_en
        return self.descricao_pt

    def __str__(self):
        return f"{self.servico.nome_pt} - {self.titulo_pt}"
