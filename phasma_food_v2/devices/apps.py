from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevicesConfig(AppConfig):
    name = "phasma_food_v2.devices"
    verbose_name = _("Devices")

    def ready(self):
        try:
            import phasma_food_project.devices.signals  # noqa F401
        except ImportError:
            pass
