from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from ._measurement import Measurement


class Result(models.Model):
    measurement = models.OneToOneField(Measurement,
                                       on_delete=models.CASCADE,
                                       primary_key=True,
                                       related_name="result"
                                       )
    data = JSONField(null=True,
                     blank=True,
                     help_text=_("Result of trained measurement.")
                     )
    date_created = models.DateTimeField(_('date created'),
                                        default=timezone.now,
                                        help_text=_("Date when result was created.")
                                        )

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return str(self.measurement_id)
