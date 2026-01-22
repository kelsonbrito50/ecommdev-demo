from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaPortfolio, Case, CaseImage, Tag


class CaseImageInline(admin.TabularInline):
    """Inline for gallery images."""
    model = CaseImage
    extra = 3
    fields = ['imagem', 'titulo', 'ordem']
    ordering = ['ordem']


@admin.register(CategoriaPortfolio)
class CategoriaPortfolioAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'slug', 'ordem']
    list_editable = ['ordem']
    prepopulated_fields = {'slug': ('nome_pt',)}
    search_fields = ['nome_pt', 'nome_en']
    ordering = ['ordem']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['titulo_pt', 'categoria', 'cliente', 'destaque', 'ativo', 'visualizacoes', 'ordem']
    list_filter = ['categoria', 'destaque', 'ativo', 'created_at']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['titulo_pt', 'titulo_en', 'cliente', 'desafio_pt', 'solucao_pt']
    prepopulated_fields = {'slug': ('titulo_pt',)}
    readonly_fields = ['visualizacoes', 'created_at', 'updated_at']
    ordering = ['-destaque', 'ordem']
    inlines = [CaseImageInline]

    fieldsets = (
        ('Identificacao', {
            'fields': ('categoria', 'titulo_pt', 'titulo_en', 'slug')
        }),
        ('Cliente', {
            'fields': ('cliente', 'industria')
        }),
        ('Case Study', {
            'fields': ('desafio_pt', 'desafio_en', 'solucao_pt', 'solucao_en', 'resultados_pt', 'resultados_en')
        }),
        ('Tecnico', {
            'fields': ('tecnologias', 'funcionalidades', 'tempo_desenvolvimento')
        }),
        ('Midia', {
            'fields': ('imagem_destaque', 'imagens', 'url_projeto')
        }),
        ('Metricas', {
            'fields': ('metricas', 'visualizacoes')
        }),
        ('Exibicao', {
            'fields': ('destaque', 'ativo', 'ordem')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']
