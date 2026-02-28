from django.contrib import admin
from django.utils.html import format_html

from .models import AvaliacaoTicket, RespostaTicket, Ticket


class RespostaTicketInline(admin.TabularInline):
    model = RespostaTicket
    extra = 1
    fields = ["autor", "conteudo", "interno", "created_at"]
    readonly_fields = ["created_at"]


class AvaliacaoTicketInline(admin.StackedInline):
    model = AvaliacaoTicket
    can_delete = False
    readonly_fields = ["nota", "comentario", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "numero",
        "assunto",
        "cliente",
        "categoria",
        "prioridade_badge",
        "status_badge",
        "atendente",
        "created_at",
    ]
    list_filter = ["status", "prioridade", "categoria", "created_at"]
    search_fields = ["numero", "assunto", "descricao", "cliente__email"]
    readonly_fields = [
        "numero",
        "created_at",
        "updated_at",
        "data_primeira_resposta",
        "data_resolucao",
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    inlines = [RespostaTicketInline, AvaliacaoTicketInline]

    fieldsets = (
        ("Identificacao", {"fields": ("numero", "status", "cliente", "atendente")}),
        ("Ticket", {"fields": ("assunto", "descricao", "categoria", "prioridade", "projeto")}),
        ("Anexos", {"fields": ("anexos",), "classes": ("collapse",)}),
        (
            "Tracking",
            {
                "fields": ("data_primeira_resposta", "data_resolucao", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def prioridade_badge(self, obj):
        colors = {
            "baixa": "secondary",
            "media": "info",
            "alta": "warning",
            "urgente": "danger",
        }
        color = colors.get(obj.prioridade, "secondary")
        return format_html(
            '<span class="badge bg-{}">{}</span>', color, obj.get_prioridade_display()
        )

    prioridade_badge.short_description = "Prioridade"

    def status_badge(self, obj):
        colors = {
            "aberto": "primary",
            "em_atendimento": "info",
            "aguardando_cliente": "warning",
            "resolvido": "success",
            "fechado": "dark",
        }
        color = colors.get(obj.status, "secondary")
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())

    status_badge.short_description = "Status"


@admin.register(RespostaTicket)
class RespostaTicketAdmin(admin.ModelAdmin):
    list_display = ["ticket", "autor", "conteudo_preview", "interno", "created_at"]
    list_filter = ["interno", "created_at"]
    search_fields = ["conteudo", "ticket__numero", "autor__email"]
    ordering = ["-created_at"]

    def conteudo_preview(self, obj):
        return obj.conteudo[:50] + "..." if len(obj.conteudo) > 50 else obj.conteudo

    conteudo_preview.short_description = "Resposta"


@admin.register(AvaliacaoTicket)
class AvaliacaoTicketAdmin(admin.ModelAdmin):
    list_display = ["ticket", "nota_stars", "created_at"]
    list_filter = ["nota", "created_at"]
    readonly_fields = ["ticket", "nota", "comentario", "created_at"]
    ordering = ["-created_at"]

    def nota_stars(self, obj):
        stars = '<span style="color: gold;">★</span>' * obj.nota
        empty = '<span style="color: #ccc;">★</span>' * (5 - obj.nota)
        return format_html(stars + empty)

    nota_stars.short_description = "Nota"

    def has_add_permission(self, request):
        return False
