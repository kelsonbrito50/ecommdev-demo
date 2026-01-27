from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import CategoriaPortfolio, Case, CaseImage, Tag


class CaseImageInline(admin.TabularInline):
    """Inline for gallery images with preview."""
    model = CaseImage
    extra = 3
    fields = ['imagem', 'imagem_preview', 'titulo', 'ordem']
    readonly_fields = ['imagem_preview']
    ordering = ['ordem']
    classes = ['collapse']

    def imagem_preview(self, obj):
        if obj.pk and obj.imagem:
            try:
                return format_html(
                    '<img src="{}" style="width:100px;height:60px;object-fit:cover;border-radius:4px;"/>',
                    obj.imagem.url
                )
            except ValueError:
                pass
        return '-'
    imagem_preview.short_description = _('Preview')


@admin.register(CategoriaPortfolio)
class CategoriaPortfolioAdmin(admin.ModelAdmin):
    """Admin for portfolio categories."""
    list_display = ['nome_pt', 'nome_en', 'slug', 'cases_count', 'ordem']
    list_editable = ['ordem']
    prepopulated_fields = {'slug': ('nome_pt',)}
    search_fields = ['nome_pt', 'nome_en']
    ordering = ['ordem']

    def cases_count(self, obj):
        count = obj.cases.filter(ativo=True).count()
        return format_html('<span class="badge bg-info">{}</span>', count)
    cases_count.short_description = _('Cases')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Full-featured admin for Portfolio Cases."""
    list_display = ['titulo_pt', 'imagem_preview', 'categoria', 'cliente', 'tecnologias_badges', 'destaque', 'ativo', 'visualizacoes', 'ordem']
    list_filter = ['categoria', 'destaque', 'ativo', 'created_at']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['titulo_pt', 'titulo_en', 'cliente', 'desafio_pt', 'solucao_pt']
    prepopulated_fields = {'slug': ('titulo_pt',)}
    readonly_fields = ['visualizacoes', 'created_at', 'updated_at', 'imagem_atual']
    ordering = ['-destaque', 'ordem']
    inlines = [CaseImageInline]
    save_on_top = True
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Identificação'), {
            'fields': ('categoria', ('titulo_pt', 'titulo_en'), 'slug'),
            'description': _('Título do case em português e inglês')
        }),
        (_('Cliente'), {
            'fields': (('cliente', 'industria'),),
            'description': _('Nome do cliente e setor de atuação')
        }),
        (_('O Desafio'), {
            'fields': ('desafio_pt', 'desafio_en'),
            'classes': ['wide'],
            'description': _('Qual problema o cliente enfrentava?')
        }),
        (_('A Solução'), {
            'fields': ('solucao_pt', 'solucao_en'),
            'classes': ['wide'],
            'description': _('Como resolvemos o problema?')
        }),
        (_('Resultados'), {
            'fields': ('resultados_pt', 'resultados_en'),
            'classes': ['wide'],
            'description': _('Quais foram os resultados alcançados?')
        }),
        (_('Detalhes Técnicos'), {
            'fields': ('tecnologias', 'funcionalidades', 'tempo_desenvolvimento'),
            'classes': ['collapse'],
            'description': _('Tecnologias usadas (separadas por vírgula)')
        }),
        (_('Mídia'), {
            'fields': ('imagem_destaque', 'imagem_atual', 'imagens', 'url_projeto'),
            'description': _('Imagem principal e galeria de imagens')
        }),
        (_('Métricas'), {
            'fields': ('metricas', 'visualizacoes'),
            'classes': ['collapse'],
            'description': _('Dados de performance (JSON)')
        }),
        (_('Exibição'), {
            'fields': (('destaque', 'ativo'), 'ordem'),
            'description': _('Controle de visibilidade')
        }),
        (_('Datas'), {
            'fields': (('created_at', 'updated_at'),),
            'classes': ['collapse']
        }),
    )

    def imagem_preview(self, obj):
        """Show thumbnail in list view."""
        if obj.pk and obj.imagem_destaque:
            try:
                return format_html(
                    '<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:5px;"/>',
                    obj.imagem_destaque.url
                )
            except ValueError:
                pass
        return format_html('<span style="color:#999;">Sem imagem</span>')
    imagem_preview.short_description = _('Imagem')

    def imagem_atual(self, obj):
        """Show current image in edit form."""
        if obj.pk and obj.imagem_destaque:
            try:
                return format_html(
                    '<img src="{}" style="max-width:400px;max-height:250px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);"/>',
                    obj.imagem_destaque.url
                )
            except ValueError:
                pass
        return format_html('<span style="color:#999;">Nenhuma imagem cadastrada</span>')
    imagem_atual.short_description = _('Imagem Atual')

    def tecnologias_badges(self, obj):
        """Show technologies as badges."""
        if obj.tecnologias:
            # tecnologias is a JSONField (list)
            techs = obj.tecnologias[:3] if isinstance(obj.tecnologias, list) else []
            badges = ''.join([
                f'<span style="background:#e9ecef;padding:2px 6px;border-radius:10px;font-size:11px;margin-right:3px;">{t}</span>'
                for t in techs
            ])
            if isinstance(obj.tecnologias, list) and len(obj.tecnologias) > 3:
                badges += '<span style="color:#999;font-size:11px;">...</span>'
            return format_html(badges)
        return '-'
    tecnologias_badges.short_description = _('Tecnologias')

    actions = ['excluir_cases', 'ativar_cases', 'desativar_cases', 'destacar_cases', 'resetar_visualizacoes']

    def has_delete_permission(self, request, obj=None):
        return True

    @admin.action(description=_('Excluir cases selecionados'))
    def excluir_cases(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} case(s) excluído(s) com sucesso!')

    @admin.action(description=_('Ativar cases selecionados'))
    def ativar_cases(self, request, queryset):
        queryset.update(ativo=True)
        self.message_user(request, _('Cases ativados com sucesso!'))

    @admin.action(description=_('Desativar cases selecionados'))
    def desativar_cases(self, request, queryset):
        queryset.update(ativo=False)
        self.message_user(request, _('Cases desativados com sucesso!'))

    @admin.action(description=_('Destacar cases selecionados'))
    def destacar_cases(self, request, queryset):
        queryset.update(destaque=True)
        self.message_user(request, _('Cases destacados com sucesso!'))

    @admin.action(description=_('Resetar visualizações'))
    def resetar_visualizacoes(self, request, queryset):
        queryset.update(visualizacoes=0)
        self.message_user(request, _('Visualizações resetadas!'))


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    """Admin for case gallery images."""
    list_display = ['id', 'titulo', 'ordem']
    search_fields = ['titulo']
    ordering = ['ordem']
    list_per_page = 20


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for tags."""
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']
