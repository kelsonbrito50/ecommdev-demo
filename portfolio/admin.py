from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CategoriaPortfolio, Case, CaseImage, Tag


@admin.register(CategoriaPortfolio)
class CategoriaPortfolioAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'slug', 'ordem']
    prepopulated_fields = {'slug': ('nome_pt',)}
    search_fields = ['nome_pt']
    ordering = ['ordem']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['titulo_pt', 'categoria', 'cliente', 'destaque', 'ativo', 'ordem']
    list_filter = ['destaque', 'ativo']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['titulo_pt', 'cliente']
    prepopulated_fields = {'slug': ('titulo_pt',)}
    ordering = ['-destaque', 'ordem']

    fieldsets = (
        (_('Identificação'), {
            'fields': ('categoria', 'titulo_pt', 'titulo_en', 'slug')
        }),
        (_('Cliente'), {
            'fields': ('cliente', 'industria')
        }),
        (_('Conteúdo'), {
            'fields': ('desafio_pt', 'solucao_pt', 'resultados_pt'),
            'classes': ['wide']
        }),
        (_('Técnico'), {
            'fields': ('tecnologias', 'funcionalidades', 'tempo_desenvolvimento'),
            'classes': ['collapse']
        }),
        (_('Mídia'), {
            'fields': ('imagem_destaque', 'url_projeto')
        }),
        (_('Exibição'), {
            'fields': ('destaque', 'ativo', 'ordem')
        }),
    )


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'ordem']
    ordering = ['ordem']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
