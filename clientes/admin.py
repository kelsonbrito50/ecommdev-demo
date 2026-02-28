from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import LogLogin, PerfilEmpresa, SessaoAtiva, Usuario


class PerfilEmpresaInline(admin.StackedInline):
    model = PerfilEmpresa
    can_delete = False
    verbose_name = "Perfil Empresa"


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ["email", "nome_completo", "is_active", "is_staff", "created_at"]
    list_filter = ["is_active", "is_staff", "is_superuser", "idioma_preferido", "created_at"]
    search_fields = ["email", "nome_completo", "telefone", "cpf"]
    ordering = ["-created_at"]
    inlines = [PerfilEmpresaInline]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informacoes Pessoais"), {"fields": ("nome_completo", "telefone", "cpf", "foto")}),
        (
            _("Preferencias"),
            {
                "fields": (
                    "idioma_preferido",
                    "notificacoes_email",
                    "notificacoes_sms",
                    "two_factor_enabled",
                )
            },
        ),
        (
            _("Permissoes"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Datas"), {"fields": ("last_login", "created_at"), "classes": ("collapse",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome_completo",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "last_login"]


@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "nome_empresa", "cnpj", "cidade", "estado"]
    search_fields = ["nome_empresa", "cnpj", "usuario__email"]
    list_filter = ["estado"]


@admin.register(LogLogin)
class LogLoginAdmin(admin.ModelAdmin):
    list_display = ["usuario", "ip_address", "dispositivo", "sucesso", "created_at"]
    list_filter = ["sucesso", "created_at"]
    search_fields = ["usuario__email", "ip_address"]
    readonly_fields = [
        "usuario",
        "ip_address",
        "user_agent",
        "dispositivo",
        "localizacao",
        "sucesso",
        "created_at",
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False


@admin.register(SessaoAtiva)
class SessaoAtivaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "dispositivo", "navegador", "ip_address", "ultimo_acesso"]
    list_filter = ["navegador", "ultimo_acesso"]
    search_fields = ["usuario__email", "ip_address", "dispositivo"]
    readonly_fields = [
        "usuario",
        "session_key",
        "ip_address",
        "dispositivo",
        "navegador",
        "ultimo_acesso",
        "created_at",
    ]
    ordering = ["-ultimo_acesso"]

    def has_add_permission(self, request):
        return False
