from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Servico, RecursoServico


class RecursoServicoInline(admin.TabularInline):
    """Inline editor for service features."""
    model = RecursoServico
    extra = 3
    fields = ['titulo_pt', 'titulo_en', 'descricao_pt', 'descricao_en', 'icone', 'ordem']
    ordering = ['ordem']
    classes = ['collapse']


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    """Full-featured admin for Services."""
    list_display = ['nome_pt', 'tipo', 'imagem_preview', 'ativo', 'destaque', 'recursos_count', 'ordem']
    list_filter = ['tipo', 'ativo', 'destaque']
    list_editable = ['ativo', 'destaque', 'ordem']
    search_fields = ['nome_pt', 'nome_en', 'descricao_pt', 'descricao_en']
    prepopulated_fields = {'slug': ('nome_pt',)}
    ordering = ['ordem']
    inlines = [RecursoServicoInline]
    save_on_top = True
    list_per_page = 20

    fieldsets = (
        (_('Identificação'), {
            'fields': ('tipo', ('nome_pt', 'nome_en'), 'slug'),
            'description': _('Informações básicas do serviço')
        }),
        (_('Descrição Curta'), {
            'fields': ('descricao_curta_pt', 'descricao_curta_en'),
            'description': _('Texto curto para listagens (máx. 200 caracteres)')
        }),
        (_('Descrição Completa'), {
            'fields': ('descricao_pt', 'descricao_en'),
            'classes': ['wide'],
            'description': _('Descrição detalhada do serviço')
        }),
        (_('Visual'), {
            'fields': ('icone', 'imagem', 'imagem_atual'),
            'description': _('Ícone (Bootstrap Icons) e imagem de destaque')
        }),
        (_('Informações Técnicas'), {
            'fields': ('tecnologias', 'beneficios_pt', 'beneficios_en'),
            'classes': ['collapse'],
            'description': _('Lista de tecnologias separadas por vírgula')
        }),
        (_('Exibição'), {
            'fields': (('ativo', 'destaque'), 'ordem'),
            'description': _('Controle de visibilidade e ordenação')
        }),
    )

    readonly_fields = ['imagem_atual']

    def imagem_preview(self, obj):
        """Show thumbnail in list view."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:5px;"/>',
                obj.imagem.url
            )
        return format_html('<span style="color:#999;">Sem imagem</span>')
    imagem_preview.short_description = _('Imagem')

    def imagem_atual(self, obj):
        """Show current image in edit form."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:200px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);"/>',
                obj.imagem.url
            )
        return format_html('<span style="color:#999;">Nenhuma imagem cadastrada</span>')
    imagem_atual.short_description = _('Imagem Atual')

    def recursos_count(self, obj):
        """Show feature count."""
        count = obj.recursos.count()
        return format_html('<span class="badge bg-info">{}</span>', count)
    recursos_count.short_description = _('Recursos')

    actions = ['ativar_servicos', 'desativar_servicos', 'destacar_servicos']

    @admin.action(description=_('Ativar serviços selecionados'))
    def ativar_servicos(self, request, queryset):
        queryset.update(ativo=True)
        self.message_user(request, _('Serviços ativados com sucesso!'))

    @admin.action(description=_('Desativar serviços selecionados'))
    def desativar_servicos(self, request, queryset):
        queryset.update(ativo=False)
        self.message_user(request, _('Serviços desativados com sucesso!'))

    @admin.action(description=_('Destacar serviços selecionados'))
    def destacar_servicos(self, request, queryset):
        queryset.update(destaque=True)
        self.message_user(request, _('Serviços destacados com sucesso!'))


@admin.register(RecursoServico)
class RecursoServicoAdmin(admin.ModelAdmin):
    """Admin for individual service features."""
    list_display = ['servico', 'titulo_pt', 'icone_display', 'ordem']
    list_filter = ['servico']
    list_editable = ['ordem']
    search_fields = ['titulo_pt', 'titulo_en', 'descricao_pt']
    ordering = ['servico', 'ordem']
    list_per_page = 30

    def icone_display(self, obj):
        if obj.icone:
            return format_html('<i class="bi bi-{}"></i> {}', obj.icone, obj.icone)
        return '-'
    icone_display.short_description = _('Ícone')
