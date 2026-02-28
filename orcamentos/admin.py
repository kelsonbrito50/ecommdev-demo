from django.contrib import admin
from django.utils.html import format_html

from .models import HistoricoOrcamento, Orcamento


class HistoricoOrcamentoInline(admin.TabularInline):
    model = HistoricoOrcamento
    extra = 0
    readonly_fields = [
        "usuario",
        "acao",
        "status_anterior",
        "status_novo",
        "observacao",
        "created_at",
    ]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = [
        "numero",
        "nome_completo",
        "tipo_projeto",
        "status_badge",
        "valor_proposto_display",
        "created_at",
    ]
    list_filter = ["status", "tipo_projeto", "created_at"]
    search_fields = ["numero", "nome_completo", "email", "empresa"]
    readonly_fields = ["numero", "created_at", "updated_at", "ip_address"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    inlines = [HistoricoOrcamentoInline]

    fieldsets = (
        ("Identificacao", {"fields": ("numero", "status", "cliente")}),
        (
            "Dados do Cliente",
            {
                "fields": (
                    "nome_completo",
                    "email",
                    "telefone",
                    "empresa",
                    "cnpj",
                    "cidade",
                    "estado",
                )
            },
        ),
        (
            "Projeto",
            {
                "fields": (
                    "tipo_projeto",
                    "pacote",
                    "descricao_projeto",
                    "objetivos",
                    "publico_alvo",
                )
            },
        ),
        (
            "Requisitos Tecnicos",
            {
                "fields": (
                    "funcionalidades",
                    "integracoes",
                    "sistema_pagamento",
                    "referencia_design",
                    "possui_dominio",
                    "possui_hospedagem",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Orcamento e Prazo",
            {"fields": ("orcamento_disponivel", "prazo_desejado", "data_inicio_preferida")},
        ),
        ("Proposta", {"fields": ("valor_proposto", "observacoes_internas")}),
        (
            "Metadados",
            {
                "fields": ("ip_address", "origem", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def status_badge(self, obj):
        colors = {
            "novo": "primary",
            "em_analise": "info",
            "aguardando_info": "warning",
            "proposta_enviada": "secondary",
            "aprovado": "success",
            "rejeitado": "danger",
            "cancelado": "dark",
        }
        color = colors.get(obj.status, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())

    status_badge.short_description = "Status"

    def valor_proposto_display(self, obj):
        if obj.valor_proposto:
            return format_html("R$ {:,.2f}", obj.valor_proposto)
        return "-"

    valor_proposto_display.short_description = "Valor Proposto"


@admin.register(HistoricoOrcamento)
class HistoricoOrcamentoAdmin(admin.ModelAdmin):
    list_display = ["orcamento", "acao", "usuario", "created_at"]
    list_filter = ["acao", "created_at"]
    search_fields = ["orcamento__numero", "observacao"]
    readonly_fields = [
        "orcamento",
        "usuario",
        "acao",
        "status_anterior",
        "status_novo",
        "observacao",
        "created_at",
    ]
    ordering = ["-created_at"]
