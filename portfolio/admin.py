from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CategoriaPortfolio, Case, CaseImage, Tag


@admin.register(CategoriaPortfolio)
class CategoriaPortfolioAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'slug', 'ordem']
    list_editable = ['ordem']
    prepopulated_fields = {'slug': ('nome_pt',)}
    search_fields = ['nome_pt']
    ordering = ['ordem']


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 3
    fields = ['imagem', 'titulo', 'ordem']
    ordering = ['ordem']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['titulo_pt', 'categoria', 'cliente', 'destaque', 'ativo', 'ordem']
    list_filter = ['categoria', 'destaque', 'ativo']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['titulo_pt', 'cliente']
    prepopulated_fields = {'slug': ('titulo_pt',)}
    ordering = ['-destaque', 'ordem']
    inlines = [CaseImageInline]
    save_on_top = True

    fieldsets = (
        (_('Identificação'), {
            'fields': ('categoria', 'titulo_pt', 'titulo_en', 'slug')
        }),
        (_('Cliente'), {
            'fields': ('cliente', 'industria')
        }),
        (_('Conteúdo'), {
            'fields': ('desafio_pt', 'desafio_en', 'solucao_pt', 'solucao_en', 'resultados_pt', 'resultados_en')
        }),
        (_('Técnico'), {
            'fields': ('tecnologias', 'funcionalidades', 'tempo_desenvolvimento')
        }),
        (_('Mídia'), {
            'fields': ('imagem_destaque', 'imagens', 'url_projeto')
        }),
        (_('Métricas'), {
            'fields': ('metricas', 'visualizacoes')
        }),
        (_('Exibição'), {
            'fields': ('destaque', 'ativo', 'ordem')
        }),
    )

    readonly_fields = ['visualizacoes']


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'case', 'titulo', 'ordem']
    list_filter = ['case']
    list_editable = ['ordem']
    search_fields = ['titulo']
    ordering = ['case', 'ordem']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']
