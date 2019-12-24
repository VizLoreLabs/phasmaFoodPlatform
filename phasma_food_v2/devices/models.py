from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PhasmaDevice(models.Model):
    mac = models.CharField(_('media access control address'),
                           max_length=127,
                           primary_key=True,
                           help_text=_("MAC (Media Access Control) address of phasma device.")
                           )
    name = models.CharField(_('name'),
                            max_length=127,
                            help_text=_("Name of phasma device.")
                            )
    date_added = models.DateTimeField(_('date added'),
                                      default=timezone.now,
                                      help_text=_("Date when phasma device was added.")
                                      )
    date_updated = models.DateTimeField(_('date updated'),
                                        auto_now=True,
                                        help_text=_("Date when phasma device was updated.")
                                        )

    class Meta:
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.mac
