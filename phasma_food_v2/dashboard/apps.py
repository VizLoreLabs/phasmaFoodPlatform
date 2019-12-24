from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    name = "phasma_food_v2.dashboard"
    verbose_name = _("Dashboard")
