from django.contrib import admin
from django.utils.html import format_html

from .models import ConfiguracaoNotificacao, LogEmail, Notificacao


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ["usuario", "tipo_badge", "categoria", "titulo", "lida", "created_at"]
    list_filter = ["tipo", "categoria", "lida", "created_at"]
    list_editable = ["lida"]
    search_fields = ["titulo", "mensagem", "usuario__email"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    def tipo_badge(self, obj):
        colors = {
            "info": "info",
            "sucesso": "success",
            "aviso": "warning",
            "erro": "danger",
        }
        color = colors.get(obj.tipo, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_tipo_display())

    tipo_badge.short_description = "Tipo"


@admin.register(LogEmail)
class LogEmailAdmin(admin.ModelAdmin):
    list_display = ["tipo", "destinatario", "assunto", "status_badge", "tentativas", "enviado_at"]
    list_filter = ["status", "tipo", "created_at"]
    search_fields = ["destinatario", "assunto", "conteudo"]
    readonly_fields = [
        "destinatario",
        "tipo",
        "assunto",
        "conteudo",
        "status",
        "erro",
        "tentativas",
        "enviado_at",
        "created_at",
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    def status_badge(self, obj):
        colors = {
            "enviado": "success",
            "falha": "danger",
            "pendente": "warning",
        }
        color = colors.get(obj.status, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())

    status_badge.short_description = "Status"

    def has_add_permission(self, request):
        return False


@admin.register(ConfiguracaoNotificacao)
class ConfiguracaoNotificacaoAdmin(admin.ModelAdmin):
    list_display = [
        "usuario",
        "email_atualizacao_projeto",
        "email_nova_fatura",
        "email_resposta_ticket",
        "email_newsletter",
    ]
    list_filter = ["email_newsletter", "email_marketing"]
    search_fields = ["usuario__email", "usuario__nome_completo"]

    fieldsets = (
        ("Usuario", {"fields": ("usuario",)}),
        (
            "Notificacoes por Email",
            {
                "fields": (
                    "email_atualizacao_projeto",
                    "email_nova_fatura",
                    "email_resposta_ticket",
                    "email_newsletter",
                    "email_marketing",
                )
            },
        ),
        (
            "Notificacoes Push",
            {"fields": ("push_atualizacao_projeto", "push_nova_fatura", "push_resposta_ticket")},
        ),
    )
