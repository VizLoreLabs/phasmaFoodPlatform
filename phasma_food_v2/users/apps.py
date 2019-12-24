from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "phasma_food_v2.users"
    verbose_name = _("Users")
