from django.contrib import admin
from django.utils.html import format_html
from .models import Projeto, Milestone, TimelineEvento, MensagemProjeto, ArquivoProjeto


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1
    fields = ['titulo', 'status', 'data_previsao', 'data_conclusao', 'ordem']


class TimelineEventoInline(admin.TabularInline):
    model = TimelineEvento
    extra = 0
    readonly_fields = ['tipo', 'titulo', 'descricao', 'usuario', 'created_at']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'status_badge', 'progresso_bar', 'valor_display', 'data_inicio', 'data_previsao']
    list_filter = ['status', 'data_inicio', 'created_at']
    search_fields = ['nome', 'cliente__email', 'cliente__nome_completo']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['equipe']
    inlines = [MilestoneInline, TimelineEventoInline]

    fieldsets = (
        ('Identificacao', {
            'fields': ('nome', 'slug', 'descricao', 'tecnologias')
        }),
        ('Referencias', {
            'fields': ('cliente', 'orcamento', 'pacote')
        }),
        ('Status', {
            'fields': ('status', 'progresso')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_previsao', 'data_conclusao')
        }),
        ('Equipe', {
            'fields': ('responsavel', 'equipe')
        }),
        ('Financeiro', {
            'fields': ('valor_total', 'observacoes')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'orcamento': 'secondary',
            'aprovado': 'info',
            'em_desenvolvimento': 'primary',
            'em_testes': 'warning',
            'revisao': 'warning',
            'concluido': 'success',
            'em_manutencao': 'info',
            'pausado': 'dark',
            'cancelado': 'danger',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'

    def progresso_bar(self, obj):
        color = 'success' if obj.progresso >= 75 else 'warning' if obj.progresso >= 50 else 'info'
        return format_html(
            '<div style="width:100px;background:#eee;border-radius:3px;">'
            '<div style="width:{}%;background:var(--bs-{});height:20px;border-radius:3px;text-align:center;color:white;font-size:12px;line-height:20px;">'
            '{}%</div></div>',
            obj.progresso, color, obj.progresso
        )
    progresso_bar.short_description = 'Progresso'

    def valor_display(self, obj):
        return format_html('R$ {:,.2f}', obj.valor_total)
    valor_display.short_description = 'Valor'


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'titulo', 'status', 'data_previsao', 'data_conclusao', 'ordem']
    list_filter = ['status', 'data_previsao']
    list_editable = ['status', 'ordem']
    search_fields = ['titulo', 'projeto__nome']
    ordering = ['projeto', 'ordem']


@admin.register(TimelineEvento)
class TimelineEventoAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'tipo', 'titulo', 'usuario', 'created_at']
    list_filter = ['tipo', 'created_at']
    search_fields = ['titulo', 'descricao', 'projeto__nome']
    readonly_fields = ['projeto', 'tipo', 'titulo', 'descricao', 'usuario', 'created_at']
    ordering = ['-created_at']


@admin.register(MensagemProjeto)
class MensagemProjetoAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'autor', 'conteudo_preview', 'lido', 'created_at']
    list_filter = ['lido', 'created_at']
    list_editable = ['lido']
    search_fields = ['conteudo', 'projeto__nome', 'autor__email']
    ordering = ['-created_at']

    def conteudo_preview(self, obj):
        return obj.conteudo[:50] + '...' if len(obj.conteudo) > 50 else obj.conteudo
    conteudo_preview.short_description = 'Mensagem'


@admin.register(ArquivoProjeto)
class ArquivoProjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'projeto', 'tipo', 'enviado_por', 'created_at']
    list_filter = ['tipo', 'created_at']
    search_fields = ['nome', 'descricao', 'projeto__nome']
    ordering = ['-created_at']
