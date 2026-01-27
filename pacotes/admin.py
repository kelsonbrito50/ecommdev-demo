from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Pacote, RecursoPacote, Adicional


class RecursoPacoteInline(admin.TabularInline):
    """Inline editor for package features."""
    model = RecursoPacote
    extra = 5
    fields = ['titulo_pt', 'titulo_en', 'incluido', 'destaque', 'ordem']
    ordering = ['ordem']
    classes = ['collapse']


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    """Full-featured admin for Pricing Packages."""
    list_display = ['nome_pt', 'tipo', 'preco_display', 'economia_display', 'suporte_dias', 'recursos_count', 'destaque', 'ativo', 'ordem']
    list_filter = ['tipo', 'destaque', 'ativo']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['nome_pt', 'nome_en', 'descricao_pt', 'descricao_en']
    ordering = ['ordem', 'preco']
    inlines = [RecursoPacoteInline]
    save_on_top = True
    list_per_page = 20

    fieldsets = (
        (_('Identificação'), {
            'fields': ('tipo', ('nome_pt', 'nome_en'), ('subtitulo_pt', 'subtitulo_en')),
            'description': _('Nome e subtítulo do pacote em português e inglês')
        }),
        (_('Descrição'), {
            'fields': ('descricao_pt', 'descricao_en'),
            'classes': ['wide'],
            'description': _('Descrição detalhada do pacote')
        }),
        (_('Preços'), {
            'fields': (('preco', 'preco_promocional'),),
            'description': _('Preço normal e preço promocional (opcional)')
        }),
        (_('Detalhes do Pacote'), {
            'fields': (('tempo_desenvolvimento', 'suporte_dias', 'horas_treinamento'),),
            'description': _('Tempo estimado, dias de suporte e horas de treinamento')
        }),
        (_('Exibição'), {
            'fields': (('destaque', 'ativo'), ('cor_destaque', 'icone'), 'ordem'),
            'description': _('Controle de visibilidade e destaque')
        }),
    )

    def preco_display(self, obj):
        """Show price with promotional price if exists."""
        if obj.preco_promocional:
            return format_html(
                '<span style="text-decoration:line-through;color:#999;font-size:12px;">R$ {:,.2f}</span><br>'
                '<strong style="color:#28a745;font-size:14px;">R$ {:,.2f}</strong>',
                obj.preco, obj.preco_promocional
            )
        return format_html('<strong>R$ {:,.2f}</strong>', obj.preco)
    preco_display.short_description = _('Preço')
    preco_display.admin_order_field = 'preco'

    def economia_display(self, obj):
        """Show savings percentage if promotional price exists."""
        if obj.preco_promocional and obj.preco > 0:
            economia = ((obj.preco - obj.preco_promocional) / obj.preco) * 100
            return format_html(
                '<span style="background:#28a745;color:white;padding:2px 8px;border-radius:10px;font-size:11px;">'
                '-{:.0f}%</span>',
                economia
            )
        return '-'
    economia_display.short_description = _('Economia')

    def recursos_count(self, obj):
        """Show feature count with included/total."""
        total = obj.recursos.count()
        incluidos = obj.recursos.filter(incluido=True).count()
        return format_html(
            '<span class="badge bg-success">{}</span>/<span class="badge bg-secondary">{}</span>',
            incluidos, total
        )
    recursos_count.short_description = _('Recursos')

    actions = ['ativar_pacotes', 'desativar_pacotes', 'destacar_pacote', 'copiar_pacote']

    @admin.action(description=_('Ativar pacotes selecionados'))
    def ativar_pacotes(self, request, queryset):
        queryset.update(ativo=True)
        self.message_user(request, _('Pacotes ativados com sucesso!'))

    @admin.action(description=_('Desativar pacotes selecionados'))
    def desativar_pacotes(self, request, queryset):
        queryset.update(ativo=False)
        self.message_user(request, _('Pacotes desativados com sucesso!'))

    @admin.action(description=_('Definir como pacote destacado'))
    def destacar_pacote(self, request, queryset):
        # Remove destaque dos outros
        Pacote.objects.update(destaque=False)
        # Destaca apenas o primeiro selecionado
        queryset[:1].update(destaque=True)
        self.message_user(request, _('Pacote destacado com sucesso!'))

    @admin.action(description=_('Duplicar pacote selecionado'))
    def copiar_pacote(self, request, queryset):
        for pacote in queryset:
            recursos = list(pacote.recursos.all())
            pacote.pk = None
            pacote.tipo = f"{pacote.tipo}_copia"
            pacote.nome_pt = f"{pacote.nome_pt} (Cópia)"
            pacote.save()
            for recurso in recursos:
                recurso.pk = None
                recurso.pacote = pacote
                recurso.save()
        self.message_user(request, _('Pacote(s) duplicado(s) com sucesso!'))


@admin.register(RecursoPacote)
class RecursoPacoteAdmin(admin.ModelAdmin):
    """Admin for individual package features."""
    list_display = ['pacote', 'titulo_pt', 'incluido_icon', 'destaque_icon', 'ordem']
    list_filter = ['pacote', 'incluido', 'destaque']
    list_editable = ['ordem']
    search_fields = ['titulo_pt', 'titulo_en']
    ordering = ['pacote', 'ordem']
    list_per_page = 50

    def incluido_icon(self, obj):
        if obj.incluido:
            return format_html('<span style="color:#28a745;font-size:18px;">✓</span>')
        return format_html('<span style="color:#dc3545;font-size:18px;">✗</span>')
    incluido_icon.short_description = _('Incluído')

    def destaque_icon(self, obj):
        if obj.destaque:
            return format_html('<span style="color:#ffc107;font-size:18px;">★</span>')
        return format_html('<span style="color:#ddd;font-size:18px;">☆</span>')
    destaque_icon.short_description = _('Destaque')

    actions = ['marcar_incluido', 'marcar_nao_incluido', 'marcar_destaque']

    @admin.action(description=_('Marcar como incluído'))
    def marcar_incluido(self, request, queryset):
        queryset.update(incluido=True)

    @admin.action(description=_('Marcar como NÃO incluído'))
    def marcar_nao_incluido(self, request, queryset):
        queryset.update(incluido=False)

    @admin.action(description=_('Marcar como destaque'))
    def marcar_destaque(self, request, queryset):
        queryset.update(destaque=True)


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    """Admin for add-on services."""
    list_display = ['nome_pt', 'preco_display', 'tipo_cobranca_badge', 'ativo', 'ordem']
    list_filter = ['tipo_cobranca', 'ativo']
    list_editable = ['ativo', 'ordem']
    search_fields = ['nome_pt', 'nome_en', 'descricao_pt']
    ordering = ['ordem']
    save_on_top = True

    fieldsets = (
        (_('Identificação'), {
            'fields': (('nome_pt', 'nome_en'),)
        }),
        (_('Descrição'), {
            'fields': ('descricao_pt', 'descricao_en')
        }),
        (_('Preço'), {
            'fields': (('preco', 'tipo_cobranca'),)
        }),
        (_('Exibição'), {
            'fields': (('ativo', 'ordem'),)
        }),
    )

    def preco_display(self, obj):
        suffix = ''
        if obj.tipo_cobranca == 'mensal':
            suffix = '/mês'
        elif obj.tipo_cobranca == 'hora':
            suffix = '/hora'
        return format_html('<strong>R$ {:,.2f}</strong>{}', obj.preco, suffix)
    preco_display.short_description = _('Preço')
    preco_display.admin_order_field = 'preco'

    def tipo_cobranca_badge(self, obj):
        colors = {'unico': 'primary', 'mensal': 'success', 'hora': 'warning'}
        color = colors.get(obj.tipo_cobranca, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.get_tipo_cobranca_display()
        )
    tipo_cobranca_badge.short_description = _('Tipo')
