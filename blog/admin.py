from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaBlog, TagBlog, Post, Comentario


@admin.register(CategoriaBlog)
class CategoriaBlogAdmin(admin.ModelAdmin):
    list_display = ['nome_pt', 'slug', 'cor_display', 'ordem']
    list_editable = ['ordem']
    prepopulated_fields = {'slug': ('nome_pt',)}
    search_fields = ['nome_pt', 'nome_en']
    ordering = ['ordem']

    def cor_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 2px 10px; border-radius: 3px;">{}</span>',
            obj.cor, obj.cor
        )
    cor_display.short_description = 'Cor'


@admin.register(TagBlog)
class TagBlogAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ['autor', 'nome', 'conteudo', 'aprovado', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo_pt', 'autor', 'categoria', 'status_badge', 'destaque', 'visualizacoes', 'data_publicacao']
    list_filter = ['status', 'categoria', 'destaque', 'data_publicacao', 'autor']
    list_editable = ['destaque']
    search_fields = ['titulo_pt', 'titulo_en', 'resumo_pt', 'conteudo_pt']
    prepopulated_fields = {'slug': ('titulo_pt',)}
    readonly_fields = ['visualizacoes', 'tempo_leitura', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
    ordering = ['-data_publicacao']
    date_hierarchy = 'data_publicacao'
    inlines = [ComentarioInline]

    fieldsets = (
        ('Identificacao', {
            'fields': ('autor', 'categoria', 'tags', 'status', 'data_publicacao')
        }),
        ('Conteudo PT', {
            'fields': ('titulo_pt', 'slug', 'resumo_pt', 'conteudo_pt')
        }),
        ('Conteudo EN', {
            'fields': ('titulo_en', 'resumo_en', 'conteudo_en'),
            'classes': ('collapse',)
        }),
        ('Midia', {
            'fields': ('imagem_destaque',)
        }),
        ('SEO', {
            'fields': ('meta_title_pt', 'meta_title_en', 'meta_description_pt', 'meta_description_en'),
            'classes': ('collapse',)
        }),
        ('Metricas', {
            'fields': ('destaque', 'visualizacoes', 'tempo_leitura')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'rascunho': 'secondary',
            'publicado': 'success',
            'agendado': 'info',
            'arquivado': 'dark',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['post', 'autor_display', 'aprovado', 'created_at']
    list_filter = ['aprovado', 'created_at']
    list_editable = ['aprovado']
    search_fields = ['nome', 'email', 'conteudo', 'post__titulo_pt']
    ordering = ['-created_at']

    def autor_display(self, obj):
        return obj.autor or obj.nome or obj.email
    autor_display.short_description = 'Autor'
