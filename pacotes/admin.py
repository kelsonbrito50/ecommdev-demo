from django.contrib import admin
from django.utils.html import format_html
from .models import Pacote, RecursoPacote, Adicional


class RecursoPacoteInline(admin.TabularInline):
    model = RecursoPacote
    extra = 1
    fields = ['titulo_pt', 'titulo_en', 'incluido', 'destaque', 'ordem']
    ordering = ['ordem']


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'tipo', 'preco_display', 'suporte_dias', 'destaque', 'ativo', 'ordem']
    list_filter = ['tipo', 'destaque', 'ativo']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['nome_pt', 'nome_en', 'descricao_pt']
    ordering = ['ordem', 'preco']
    inlines = [RecursoPacoteInline]

    fieldsets = (
        ('Identificação', {
            'fields': ('tipo', 'nome_pt', 'nome_en', 'subtitulo_pt', 'subtitulo_en')
        }),
        ('Descrição', {
            'fields': ('descricao_pt', 'descricao_en')
        }),
        ('Preços', {
            'fields': ('preco', 'preco_promocional')
        }),
        ('Detalhes', {
            'fields': ('tempo_desenvolvimento', 'suporte_dias', 'horas_treinamento')
        }),
        ('Exibição', {
            'fields': ('destaque', 'cor_destaque', 'icone', 'ativo', 'ordem')
        }),
    )

    def preco_display(self, obj):
        if obj.preco_promocional:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">R$ {:,.2f}</span><br>'
                '<strong style="color: green;">R$ {:,.2f}</strong>',
                obj.preco, obj.preco_promocional
            )
        return format_html('R$ {:,.2f}', obj.preco)
    preco_display.short_description = 'Preço'
    preco_display.admin_order_field = 'preco'


@admin.register(RecursoPacote)
class RecursoPacoteAdmin(admin.ModelAdmin):
    list_display = ['pacote', 'titulo_pt', 'incluido', 'destaque', 'ordem']
    list_filter = ['pacote', 'incluido', 'destaque']
    list_editable = ['incluido', 'destaque', 'ordem']
    search_fields = ['titulo_pt', 'titulo_en']
    ordering = ['pacote', 'ordem']


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'preco_display', 'tipo_cobranca', 'ativo', 'ordem']
    list_filter = ['tipo_cobranca', 'ativo']
    list_editable = ['ativo', 'ordem']
    search_fields = ['nome_pt', 'nome_en']
    ordering = ['ordem']

    def preco_display(self, obj):
        suffix = ''
        if obj.tipo_cobranca == 'mensal':
            suffix = '/mês'
        elif obj.tipo_cobranca == 'hora':
            suffix = '/hora'
        return format_html('R$ {:,.2f}{}', obj.preco, suffix)
    preco_display.short_description = 'Preço'
    preco_display.admin_order_field = 'preco'
