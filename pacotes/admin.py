from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Adicional, Pacote, RecursoPacote


class RecursoPacoteInline(admin.TabularInline):
    model = RecursoPacote
    extra = 3
    fields = ["titulo_pt", "incluido", "destaque", "ordem"]
    ordering = ["ordem"]


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    list_display = ["nome_pt", "tipo", "preco", "suporte_dias", "destaque", "ativo", "ordem"]
    list_filter = ["tipo", "destaque", "ativo"]
    list_editable = ["destaque", "ativo", "ordem"]
    search_fields = ["nome_pt", "nome_en"]
    ordering = ["ordem"]
    inlines = [RecursoPacoteInline]
    save_on_top = True

    fieldsets = (
        (
            _("Identificação"),
            {"fields": ("tipo", "nome_pt", "nome_en", "subtitulo_pt", "subtitulo_en")},
        ),
        (_("Descrição"), {"fields": ("descricao_pt", "descricao_en")}),
        (_("Preços"), {"fields": ("preco", "preco_promocional")}),
        (_("Detalhes"), {"fields": ("tempo_desenvolvimento", "suporte_dias", "horas_treinamento")}),
        (_("Exibição"), {"fields": ("destaque", "ativo", "icone", "cor_destaque", "ordem")}),
    )


@admin.register(RecursoPacote)
class RecursoPacoteAdmin(admin.ModelAdmin):
    list_display = ["pacote", "titulo_pt", "incluido", "destaque", "ordem"]
    list_filter = ["pacote", "incluido", "destaque"]
    list_editable = ["incluido", "destaque", "ordem"]
    search_fields = ["titulo_pt"]
    ordering = ["pacote", "ordem"]


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ["nome_pt", "preco", "tipo_cobranca", "ativo", "ordem"]
    list_filter = ["tipo_cobranca", "ativo"]
    list_editable = ["ativo", "ordem"]
    search_fields = ["nome_pt"]
    ordering = ["ordem"]

    fieldsets = (
        (_("Identificação"), {"fields": ("nome_pt", "nome_en")}),
        (_("Descrição"), {"fields": ("descricao_pt", "descricao_en")}),
        (_("Preço"), {"fields": ("preco", "tipo_cobranca")}),
        (_("Exibição"), {"fields": ("ativo", "ordem")}),
    )
