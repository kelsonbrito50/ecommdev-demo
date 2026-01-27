from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CategoriaPortfolio, Case, CaseImage, Tag


@admin.register(CategoriaPortfolio)
class CategoriaPortfolioAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'slug', 'ordem']
    list_editable = ['ordem']
    search_fields = ['nome_pt']
    ordering = ['ordem']


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 1
    fields = ['imagem', 'titulo', 'ordem']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['titulo_pt', 'cliente', 'destaque', 'ativo', 'ordem']
    list_filter = ['destaque', 'ativo']
    list_editable = ['destaque', 'ativo', 'ordem']
    search_fields = ['titulo_pt', 'cliente']
    ordering = ['ordem']
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
            'fields': ('imagem_destaque', 'url_projeto')
        }),
        (_('Exibição'), {
            'fields': ('destaque', 'ativo', 'ordem')
        }),
    )


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'ordem']
    list_editable = ['ordem']
    search_fields = ['titulo']
    ordering = ['ordem']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    search_fields = ['nome']
