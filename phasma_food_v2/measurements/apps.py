from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MeasurementsConfig(AppConfig):
    name = 'phasma_food_v2.measurements'
    verbose_name = _("Measurements")
