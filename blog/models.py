"""
Blog App Models - Blog posts and categories
"""
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.validators import validate_image


class CategoriaBlog(models.Model):
    """Blog category."""

    nome_pt = models.CharField(_('Nome (PT)'), max_length=100)
    nome_en = models.CharField(_('Nome (EN)'), max_length=100, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    descricao_pt = models.TextField(_('Descrição (PT)'), blank=True)
    descricao_en = models.TextField(_('Descrição (EN)'), blank=True)
    icone = models.CharField(_('Ícone'), max_length=50, blank=True)
    cor = models.CharField(_('Cor'), max_length=20, default='#0066CC')
    ordem = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Categoria do Blog')
        verbose_name_plural = _('Categorias do Blog')
        ordering = ['ordem', 'nome_pt']

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


class TagBlog(models.Model):
    """Blog tag."""

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


class Post(models.Model):
    """Blog post."""

    STATUS_CHOICES = [
        ('rascunho', _('Rascunho')),
        ('publicado', _('Publicado')),
        ('agendado', _('Agendado')),
        ('arquivado', _('Arquivado')),
    ]

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name=_('Autor')
    )
    categoria = models.ForeignKey(
        CategoriaBlog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_('Categoria')
    )
    tags = models.ManyToManyField(TagBlog, blank=True, related_name='posts', verbose_name=_('Tags'))

    # Content
    titulo_pt = models.CharField(_('Título (PT)'), max_length=200)
    titulo_en = models.CharField(_('Título (EN)'), max_length=200, blank=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    resumo_pt = models.TextField(_('Resumo (PT)'), max_length=500, blank=True)
    resumo_en = models.TextField(_('Resumo (EN)'), max_length=500, blank=True)
    conteudo_pt = models.TextField(_('Conteúdo (PT)'))
    conteudo_en = models.TextField(_('Conteúdo (EN)'), blank=True)
    imagem_destaque = models.ImageField(
        _('Imagem de Destaque'),
        upload_to='blog/',
        blank=True,
        null=True,
        validators=[validate_image]
    )

    # SEO
    meta_title_pt = models.CharField(_('Meta Title (PT)'), max_length=70, blank=True)
    meta_title_en = models.CharField(_('Meta Title (EN)'), max_length=70, blank=True)
    meta_description_pt = models.CharField(_('Meta Description (PT)'), max_length=160, blank=True)
    meta_description_en = models.CharField(_('Meta Description (EN)'), max_length=160, blank=True)

    # Publishing
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='rascunho')
    data_publicacao = models.DateTimeField(_('Data de Publicação'), null=True, blank=True)
    destaque = models.BooleanField(_('Destacar na Home'), default=False)

    # Metrics
    visualizacoes = models.PositiveIntegerField(_('Visualizações'), default=0)
    tempo_leitura = models.PositiveIntegerField(_('Tempo de Leitura (min)'), default=5)

    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-data_publicacao', '-created_at']

    def __str__(self):
        return self.titulo_pt

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo_pt)
        # Calculate reading time
        word_count = len(self.conteudo_pt.split())
        self.tempo_leitura = max(1, word_count // 200)
        super().save(*args, **kwargs)

    def get_titulo(self, lang='pt-br'):
        return self.titulo_en if lang == 'en' and self.titulo_en else self.titulo_pt

    def get_conteudo(self, lang='pt-br'):
        return self.conteudo_en if lang == 'en' and self.conteudo_en else self.conteudo_pt

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:detalhe', kwargs={'slug': self.slug})

    @property
    def titulo(self):
        """Alias for template compatibility."""
        return self.titulo_pt

    @property
    def resumo(self):
        """Alias for template compatibility."""
        return self.resumo_pt

    @property
    def imagem(self):
        """Alias for template compatibility."""
        return self.imagem_destaque

    @property
    def conteudo(self):
        """Alias for template compatibility."""
        return self.conteudo_pt


class Comentario(models.Model):
    """Blog post comment (optional)."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_('Post')
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Autor')
    )
    nome = models.CharField(_('Nome'), max_length=100, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    conteudo = models.TextField(_('Comentário'))
    aprovado = models.BooleanField(_('Aprovado'), default=False)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Comentário')
        verbose_name_plural = _('Comentários')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nome or self.autor} em {self.post.titulo_pt[:30]}"
