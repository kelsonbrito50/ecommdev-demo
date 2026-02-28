from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PacotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pacotes'
    verbose_name = _('Pacotes')
