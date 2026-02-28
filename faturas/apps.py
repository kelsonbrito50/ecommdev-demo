from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FaturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faturas'
    verbose_name = _('Faturas')
