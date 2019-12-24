from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatisticConfig(AppConfig):
    name = 'phasma_food_v2.statistic'
    verbose_name = _("Statistic")
