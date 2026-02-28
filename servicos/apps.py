from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServicosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "servicos"
    verbose_name = _("Serviços")
