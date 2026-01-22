from django.contrib import admin
from django.utils.html import format_html
from .models import ConfiguracaoSite, Contato, Depoimento, FAQ


@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    list_display = ['nome_site_pt', 'email_contato', 'telefone', 'updated_at']

    fieldsets = (
        ('Identificação', {
            'fields': ('nome_site_pt', 'nome_site_en', 'tagline_pt', 'tagline_en')
        }),
        ('Descrição', {
            'fields': ('descricao_pt', 'descricao_en')
        }),
        ('Imagens', {
            'fields': ('logo', 'favicon')
        }),
        ('Contato', {
            'fields': ('email_contato', 'telefone', 'whatsapp', 'endereco', 'horario_atendimento')
        }),
        ('Redes Sociais', {
            'fields': ('linkedin', 'instagram', 'github', 'youtube')
        }),
        ('SEO', {
            'fields': ('meta_keywords', 'meta_description_pt', 'meta_description_en')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id')
        }),
    )

    def has_add_permission(self, request):
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['nome', 'email', 'assunto', 'mensagem']
    readonly_fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem', 'ip_address', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'avaliacao_stars', 'ativo', 'destaque', 'ordem']
    list_filter = ['ativo', 'destaque', 'avaliacao']
    list_editable = ['ativo', 'destaque', 'ordem']
    search_fields = ['nome', 'empresa', 'depoimento_pt']
    ordering = ['ordem']

    def avaliacao_stars(self, obj):
        stars = '<i class="bi bi-star-fill" style="color: gold;"></i>' * obj.avaliacao
        return format_html(stars)
    avaliacao_stars.short_description = 'Avaliacao'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['pergunta_pt', 'categoria', 'ativo', 'ordem']
    list_filter = ['categoria', 'ativo']
    list_editable = ['ativo', 'ordem']
    search_fields = ['pergunta_pt', 'resposta_pt']
    ordering = ['categoria', 'ordem']
