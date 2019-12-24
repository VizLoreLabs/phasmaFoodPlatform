from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField


class PlatformStatistic(models.Model):
    users = JSONField()
    platform = JSONField()
    mongo = JSONField()
    postgres = JSONField()
    date_created = models.DateTimeField(_('date created'),
                                        default=timezone.now,
                                        help_text=_("Date when statistic was created."))

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return str(self.pk)
