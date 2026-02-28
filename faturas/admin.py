from django.contrib import admin
from django.utils.html import format_html

from .models import Fatura, ItemFatura, Pagamento


class ItemFaturaInline(admin.TabularInline):
    model = ItemFatura
    extra = 1
    fields = ["descricao", "quantidade", "valor_unitario", "subtotal"]
    readonly_fields = ["subtotal"]


class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    fields = ["metodo", "valor", "status", "transacao_id", "data_pagamento"]
    readonly_fields = ["transacao_id", "data_pagamento"]


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = [
        "numero",
        "cliente",
        "projeto",
        "valor_display",
        "status_badge",
        "data_vencimento",
        "data_pagamento",
    ]
    list_filter = ["status", "data_vencimento", "data_emissao"]
    search_fields = ["numero", "cliente__email", "cliente__nome_completo", "descricao"]
    readonly_fields = ["numero", "valor_total", "data_emissao", "created_at", "updated_at"]
    ordering = ["-created_at"]
    date_hierarchy = "data_emissao"
    inlines = [ItemFaturaInline, PagamentoInline]

    fieldsets = (
        ("Identificacao", {"fields": ("numero", "status", "cliente", "projeto")}),
        ("Valores", {"fields": ("subtotal", "desconto", "impostos", "valor_total")}),
        ("Datas", {"fields": ("data_emissao", "data_vencimento", "data_pagamento")}),
        (
            "Observacoes",
            {
                "fields": ("descricao", "observacoes", "observacoes_internas"),
                "classes": ("collapse",),
            },
        ),
    )

    def valor_display(self, obj):
        return format_html("R$ {:,.2f}", obj.valor_total)

    valor_display.short_description = "Valor Total"

    def status_badge(self, obj):
        colors = {
            "rascunho": "secondary",
            "pendente": "warning",
            "paga": "success",
            "vencida": "danger",
            "cancelada": "dark",
            "reembolsada": "info",
        }
        color = colors.get(obj.status, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())

    status_badge.short_description = "Status"


@admin.register(ItemFatura)
class ItemFaturaAdmin(admin.ModelAdmin):
    list_display = ["fatura", "descricao", "quantidade", "valor_unitario", "subtotal"]
    list_filter = ["fatura__status"]
    search_fields = ["descricao", "fatura__numero"]
    readonly_fields = ["subtotal"]


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = [
        "fatura",
        "metodo",
        "valor_display",
        "status_badge",
        "gateway",
        "data_pagamento",
    ]
    list_filter = ["status", "metodo", "gateway", "created_at"]
    search_fields = ["fatura__numero", "transacao_id"]
    readonly_fields = ["transacao_id", "dados_gateway", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def valor_display(self, obj):
        return format_html("R$ {:,.2f}", obj.valor)

    valor_display.short_description = "Valor"

    def status_badge(self, obj):
        colors = {
            "pendente": "warning",
            "processando": "info",
            "aprovado": "success",
            "recusado": "danger",
            "cancelado": "dark",
            "reembolsado": "secondary",
        }
        color = colors.get(obj.status, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())

    status_badge.short_description = "Status"
