from django.contrib import admin
from .models import Servico, RecursoServico


class RecursoServicoInline(admin.TabularInline):
    model = RecursoServico
    extra = 1
    fields = ['titulo_pt', 'titulo_en', 'descricao_pt', 'icone', 'ordem']


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'tipo', 'ativo', 'destaque', 'ordem']
    list_filter = ['tipo', 'ativo', 'destaque']
    list_editable = ['ativo', 'destaque', 'ordem']
    search_fields = ['nome_pt', 'nome_en', 'descricao_pt']
    prepopulated_fields = {'slug': ('nome_pt',)}
    ordering = ['ordem']
    inlines = [RecursoServicoInline]

    fieldsets = (
        ('Identificacao', {
            'fields': ('tipo', 'nome_pt', 'nome_en', 'slug')
        }),
        ('Descricao', {
            'fields': ('descricao_curta_pt', 'descricao_curta_en', 'descricao_pt', 'descricao_en')
        }),
        ('Visual', {
            'fields': ('icone', 'imagem')
        }),
        ('Tecnico', {
            'fields': ('tecnologias', 'beneficios_pt', 'beneficios_en')
        }),
        ('Exibicao', {
            'fields': ('ativo', 'destaque', 'ordem')
        }),
    )


@admin.register(RecursoServico)
class RecursoServicoAdmin(admin.ModelAdmin):
    list_display = ['servico', 'titulo_pt', 'ordem']
    list_filter = ['servico']
    search_fields = ['titulo_pt', 'titulo_en']
    ordering = ['servico', 'ordem']
