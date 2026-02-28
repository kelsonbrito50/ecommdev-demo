from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SuporteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "suporte"
    verbose_name = _("Suporte")
