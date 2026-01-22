"""
Projetos App Models - Project management
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import validate_document


class Projeto(models.Model):
    """Client project."""

    STATUS_CHOICES = [
        ('orcamento', _('Em Orçamento')),
        ('aprovado', _('Aprovado')),
        ('em_desenvolvimento', _('Em Desenvolvimento')),
        ('em_testes', _('Em Testes')),
        ('revisao', _('Em Revisão')),
        ('concluido', _('Concluído')),
        ('em_manutencao', _('Em Manutenção')),
        ('pausado', _('Pausado')),
        ('cancelado', _('Cancelado')),
    ]

    # References
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projetos',
        verbose_name=_('Cliente')
    )
    orcamento = models.OneToOneField(
        'orcamentos.Orcamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projeto',
        verbose_name=_('Orçamento')
    )
    pacote = models.ForeignKey(
        'pacotes.Pacote',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Pacote')
    )

    # Project info
    nome = models.CharField(_('Nome do Projeto'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    descricao = models.TextField(_('Descrição'), blank=True)
    tecnologias = models.JSONField(_('Tecnologias'), default=list, blank=True)

    # Status and progress
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='aprovado')
    progresso = models.PositiveIntegerField(_('Progresso (%)'), default=0)

    # Dates
    data_inicio = models.DateField(_('Data de Início'), null=True, blank=True)
    data_previsao = models.DateField(_('Data de Previsão'), null=True, blank=True)
    data_conclusao = models.DateField(_('Data de Conclusão'), null=True, blank=True)

    # Team
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projetos_responsavel',
        verbose_name=_('Responsável')
    )
    equipe = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projetos_equipe',
        verbose_name=_('Equipe')
    )

    # Contract
    valor_total = models.DecimalField(_('Valor Total'), max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(_('Observações Internas'), blank=True)

    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Milestone(models.Model):
    """Project milestone."""

    STATUS_CHOICES = [
        ('pendente', _('Pendente')),
        ('em_andamento', _('Em Andamento')),
        ('concluido', _('Concluído')),
        ('atrasado', _('Atrasado')),
    ]

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='milestones',
        verbose_name=_('Projeto')
    )
    titulo = models.CharField(_('Título'), max_length=200)
    descricao = models.TextField(_('Descrição'), blank=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_previsao = models.DateField(_('Data Prevista'), null=True, blank=True)
    data_conclusao = models.DateField(_('Data de Conclusão'), null=True, blank=True)
    ordem = models.PositiveIntegerField(_('Ordem'), default=0)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')
        ordering = ['ordem', 'data_previsao']

    def __str__(self):
        return f"{self.projeto.nome} - {self.titulo}"


class TimelineEvento(models.Model):
    """Project timeline event."""

    TIPO_CHOICES = [
        ('criacao', _('Projeto Criado')),
        ('atualizacao', _('Atualização')),
        ('milestone', _('Milestone Concluído')),
        ('mensagem', _('Nova Mensagem')),
        ('arquivo', _('Arquivo Enviado')),
        ('status', _('Status Alterado')),
        ('reuniao', _('Reunião')),
    ]

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='timeline',
        verbose_name=_('Projeto')
    )
    tipo = models.CharField(_('Tipo'), max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(_('Título'), max_length=200)
    descricao = models.TextField(_('Descrição'), blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Usuário')
    )
    created_at = models.DateTimeField(_('Data/Hora'), auto_now_add=True)

    class Meta:
        verbose_name = _('Evento da Timeline')
        verbose_name_plural = _('Eventos da Timeline')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.projeto.nome} - {self.titulo}"


class MensagemProjeto(models.Model):
    """Project message/communication."""

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='mensagens',
        verbose_name=_('Projeto')
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Autor')
    )
    conteudo = models.TextField(_('Mensagem'))
    anexos = models.JSONField(_('Anexos'), default=list, blank=True)
    lido = models.BooleanField(_('Lido'), default=False)
    created_at = models.DateTimeField(_('Enviado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Mensagem do Projeto')
        verbose_name_plural = _('Mensagens do Projeto')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.autor} - {self.created_at}"


class ArquivoProjeto(models.Model):
    """Project file/document."""

    TIPO_CHOICES = [
        ('design', _('Design')),
        ('documento', _('Documento')),
        ('codigo', _('Código')),
        ('imagem', _('Imagem')),
        ('outro', _('Outro')),
    ]

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='arquivos',
        verbose_name=_('Projeto')
    )
    nome = models.CharField(_('Nome'), max_length=255)
    tipo = models.CharField(_('Tipo'), max_length=20, choices=TIPO_CHOICES, default='documento')
    arquivo = models.FileField(
        _('Arquivo'),
        upload_to='projetos/arquivos/',
        validators=[validate_document]
    )
    descricao = models.TextField(_('Descrição'), blank=True)
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Enviado por')
    )
    created_at = models.DateTimeField(_('Enviado em'), auto_now_add=True)

    class Meta:
        verbose_name = _('Arquivo do Projeto')
        verbose_name_plural = _('Arquivos do Projeto')
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    @property
    def tamanho(self):
        if self.arquivo:
            return self.arquivo.size
        return 0
