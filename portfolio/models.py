"""
Portfolio App Models - Case studies and projects
"""
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.validators import validate_image


class CategoriaPortfolio(models.Model):
    """Portfolio category."""

    nome_pt = models.CharField(_('Nome (PT)'), max_length=100)
    nome_en = models.CharField(_('Nome (EN)'), max_length=100, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    icone = models.CharField(_('Ícone'), max_length=50, blank=True)
    ordem = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Categoria de Portfólio')
        verbose_name_plural = _('Categorias de Portfólio')
        ordering = ['ordem']

    def __str__(self):
        return self.nome_pt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome_pt)
        super().save(*args, **kwargs)

    @property
    def nome(self):
        """Alias for template compatibility."""
        return self.nome_pt


class Case(models.Model):
    """Portfolio case study."""

    categoria = models.ForeignKey(
        CategoriaPortfolio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cases',
        verbose_name=_('Categoria')
    )
    titulo_pt = models.CharField(_('Título (PT)'), max_length=200)
    titulo_en = models.CharField(_('Título (EN)'), max_length=200, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)

    # Client info (anonymized)
    cliente = models.CharField(_('Cliente'), max_length=100, blank=True, help_text=_('Nome ou setor'))
    industria = models.CharField(_('Indústria/Setor'), max_length=100, blank=True)

    # Case details
    desafio_pt = models.TextField(_('Desafio (PT)'))
    desafio_en = models.TextField(_('Desafio (EN)'), blank=True)
    solucao_pt = models.TextField(_('Solução (PT)'))
    solucao_en = models.TextField(_('Solução (EN)'), blank=True)
    resultados_pt = models.TextField(_('Resultados (PT)'), blank=True)
    resultados_en = models.TextField(_('Resultados (EN)'), blank=True)

    # Technical
    tecnologias = models.JSONField(_('Tecnologias Utilizadas'), default=list, blank=True)
    funcionalidades = models.JSONField(_('Funcionalidades'), default=list, blank=True)
    tempo_desenvolvimento = models.CharField(_('Tempo de Desenvolvimento'), max_length=50, blank=True)

    # Media
    imagem_destaque = models.ImageField(
        _('Imagem de Destaque'),
        upload_to='portfolio/',
        blank=True,
        null=True,
        validators=[validate_image]
    )
    imagens = models.JSONField(_('Galeria de Imagens'), default=list, blank=True)
    url_projeto = models.URLField(_('URL do Projeto'), blank=True)

    # Metrics
    metricas = models.JSONField(_('Métricas de Sucesso'), default=dict, blank=True)

    # Display
    destaque = models.BooleanField(_('Destacar na Home'), default=False)
    ativo = models.BooleanField(_('Ativo'), default=True)
    ordem = models.PositiveIntegerField(_('Ordem'), default=0)
    visualizacoes = models.PositiveIntegerField(_('Visualizações'), default=0)

    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')
        ordering = ['-destaque', 'ordem', '-created_at']

    def __str__(self):
        return self.titulo_pt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo_pt)
        super().save(*args, **kwargs)

    def get_titulo(self, lang='pt-br'):
        return self.titulo_en if lang == 'en' and self.titulo_en else self.titulo_pt

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio:detalhe', kwargs={'slug': self.slug})

    @property
    def titulo(self):
        """Alias for template compatibility."""
        return self.titulo_pt

    @property
    def imagem(self):
        """Alias for template compatibility."""
        return self.imagem_destaque

    @property
    def descricao(self):
        """Full description combining desafio, solucao, resultados."""
        parts = []
        if self.desafio_pt:
            parts.append(f"<h4>Desafio</h4><p>{self.desafio_pt}</p>")
        if self.solucao_pt:
            parts.append(f"<h4>Solução</h4><p>{self.solucao_pt}</p>")
        if self.resultados_pt:
            parts.append(f"<h4>Resultados</h4><p>{self.resultados_pt}</p>")
        return ''.join(parts)

    @property
    def descricao_curta(self):
        """Short description from desafio."""
        if self.desafio_pt:
            return self.desafio_pt[:150] + '...' if len(self.desafio_pt) > 150 else self.desafio_pt
        return ''

    @property
    def cliente_nome(self):
        """Alias for template compatibility."""
        return self.cliente

    @property
    def tecnologias_lista(self):
        """Return tecnologias as comma-separated string."""
        if isinstance(self.tecnologias, list):
            return ', '.join(self.tecnologias)
        return self.tecnologias


class CaseImage(models.Model):
    """Gallery image for portfolio case."""

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='galeria',
        verbose_name=_('Case')
    )
    imagem = models.ImageField(
        _('Imagem'),
        upload_to='portfolio/galeria/',
        validators=[validate_image]
    )
    titulo = models.CharField(_('Título'), max_length=100, blank=True)
    ordem = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Imagem do Case')
        verbose_name_plural = _('Imagens do Case')
        ordering = ['ordem']

    def __str__(self):
        case_name = self.case.titulo_pt if self.case else "Sem Case"
        return f"{case_name} - {self.titulo or f'Imagem {self.pk}'}"


class Tag(models.Model):
    """Tag for portfolio cases."""

    nome = models.CharField(_('Nome'), max_length=50, unique=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


