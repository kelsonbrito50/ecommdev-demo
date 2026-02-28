"""
Core App Models - Site settings and contact
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import validate_image


class ConfiguracaoSite(models.Model):
    """Site-wide configuration settings."""

    nome_site_pt = models.CharField(_("Nome do Site (PT)"), max_length=100, default="ECOMMDEV")
    nome_site_en = models.CharField(_("Nome do Site (EN)"), max_length=100, default="ECOMMDEV")
    tagline_pt = models.CharField(_("Tagline (PT)"), max_length=255, blank=True)
    tagline_en = models.CharField(_("Tagline (EN)"), max_length=255, blank=True)
    descricao_pt = models.TextField(_("Descrição (PT)"), blank=True)
    descricao_en = models.TextField(_("Descrição (EN)"), blank=True)
    logo = models.ImageField(
        _("Logo"), upload_to="site/", blank=True, null=True, validators=[validate_image]
    )
    favicon = models.ImageField(
        _("Favicon"), upload_to="site/", blank=True, null=True, validators=[validate_image]
    )
    email_contato = models.EmailField(_("Email de Contato"), default="contato@ecommdev.com.br")
    telefone = models.CharField(_("Telefone"), max_length=20, blank=True)
    whatsapp = models.CharField(_("WhatsApp"), max_length=20, blank=True)
    endereco = models.TextField(_("Endereço"), blank=True)
    horario_atendimento = models.CharField(_("Horário de Atendimento"), max_length=100, blank=True)

    # Social Media
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    github = models.URLField(_("GitHub"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)

    # SEO
    meta_keywords = models.TextField(_("Meta Keywords"), blank=True)
    meta_description_pt = models.TextField(_("Meta Description (PT)"), blank=True)
    meta_description_en = models.TextField(_("Meta Description (EN)"), blank=True)

    # Analytics
    google_analytics_id = models.CharField(_("Google Analytics ID"), max_length=50, blank=True)
    facebook_pixel_id = models.CharField(_("Facebook Pixel ID"), max_length=50, blank=True)

    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Configuração do Site")
        verbose_name_plural = _("Configurações do Site")

    def __str__(self):
        return self.nome_site_pt

    def save(self, *args, **kwargs):
        # Ensure only one config exists
        if not self.pk and ConfiguracaoSite.objects.exists():
            raise ValueError("Já existe uma configuração do site")
        super().save(*args, **kwargs)


class Contato(models.Model):
    """Contact form submissions."""

    STATUS_CHOICES = [
        ("novo", _("Novo")),
        ("lido", _("Lido")),
        ("respondido", _("Respondido")),
        ("arquivado", _("Arquivado")),
    ]

    nome = models.CharField(_("Nome"), max_length=100)
    email = models.EmailField(_("Email"))
    telefone = models.CharField(_("Telefone"), max_length=20, blank=True)
    assunto = models.CharField(_("Assunto"), max_length=200)
    mensagem = models.TextField(_("Mensagem"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="novo")
    ip_address = models.GenericIPAddressField(_("IP"), blank=True, null=True)
    created_at = models.DateTimeField(_("Enviado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("Contato")
        verbose_name_plural = _("Contatos")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nome} - {self.assunto}"


class Depoimento(models.Model):
    """Client testimonials."""

    nome = models.CharField(_("Nome"), max_length=100)
    cargo = models.CharField(_("Cargo"), max_length=100, blank=True)
    empresa = models.CharField(_("Empresa"), max_length=100, blank=True)
    foto = models.ImageField(
        _("Foto"), upload_to="depoimentos/", blank=True, null=True, validators=[validate_image]
    )
    depoimento_pt = models.TextField(_("Depoimento (PT)"))
    depoimento_en = models.TextField(_("Depoimento (EN)"), blank=True)
    avaliacao = models.PositiveSmallIntegerField(
        _("Avaliação"), choices=[(i, str(i)) for i in range(1, 6)], default=5
    )
    ativo = models.BooleanField(_("Ativo"), default=True)
    destaque = models.BooleanField(_("Destaque"), default=False)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("Depoimento")
        verbose_name_plural = _("Depoimentos")
        ordering = ["ordem", "-created_at"]

    def __str__(self):
        return f"{self.nome} - {self.empresa}"


class FAQ(models.Model):
    """Frequently Asked Questions."""

    CATEGORIA_CHOICES = [
        ("geral", _("Geral")),
        ("servicos", _("Serviços")),
        ("pacotes", _("Pacotes")),
        ("pagamento", _("Pagamento")),
        ("suporte", _("Suporte")),
    ]

    categoria = models.CharField(
        _("Categoria"), max_length=20, choices=CATEGORIA_CHOICES, default="geral"
    )
    pergunta_pt = models.CharField(_("Pergunta (PT)"), max_length=300)
    pergunta_en = models.CharField(_("Pergunta (EN)"), max_length=300, blank=True)
    resposta_pt = models.TextField(_("Resposta (PT)"))
    resposta_en = models.TextField(_("Resposta (EN)"), blank=True)
    ativo = models.BooleanField(_("Ativo"), default=True)
    ordem = models.PositiveIntegerField(_("Ordem"), default=0)
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ["categoria", "ordem"]

    def __str__(self):
        return self.pergunta_pt[:50]

    @property
    def pergunta(self):
        from django.utils.translation import get_language

        lang = get_language()
        if lang and lang.startswith("en") and self.pergunta_en:
            return self.pergunta_en
        return self.pergunta_pt

    @property
    def resposta(self):
        from django.utils.translation import get_language

        lang = get_language()
        if lang and lang.startswith("en") and self.resposta_en:
            return self.resposta_en
        return self.resposta_pt
