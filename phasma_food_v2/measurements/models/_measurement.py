from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Measurement(models.Model):
    sample_id = models.IntegerField(primary_key=True,
                                    help_text=_("Measurement ID")
                                    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True,
                              on_delete=models.SET_NULL,
                              help_text=_("User that did measurement."),
                              related_name="measurements"
                              )
    mobile = models.ForeignKey("fcm_django.FCMDevice",
                               null=True,
                               on_delete=models.SET_NULL,
                               help_text=_("ID of mobile device form where measurement is sent."),
                               related_name="measurements"
                               )
    phasma_device = models.ForeignKey("devices.PhasmaDevice",
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      help_text=_("ID of phasma device that did measurement."),
                                      related_name="measurements"
                                      )
    laboratory = models.CharField(max_length=127,
                                  null=True,
                                  blank=True,
                                  help_text=_("Name of laboratory that is doing measurement.")
                                  )
    food_type = models.CharField(max_length=127,
                                 null=True,
                                 blank=True,
                                 help_text=_("Name of food type that is tested.")
                                 )
    food_subtype = models.CharField(max_length=127,
                                    null=True,
                                    blank=True,
                                    help_text=_("Name of food subtype that is tested if exists.")
                                    )
    use_case = models.CharField(max_length=127,
                                null=True,
                                blank=True,
                                help_text=_("Name of use case.")
                                )
    use_case_sample_id = models.CharField(max_length=127,
                                          null=True,
                                          blank=True,
                                          help_text=_("Determine id for particular use case.")
                                          )
    granularity = models.CharField(max_length=127,
                                   null=True,
                                   blank=True,
                                   help_text=_("Granularity of food samples.")
                                   )
    mycotoxins = models.CharField(max_length=127,
                                  null=True,
                                  blank=True,
                                  help_text=_("Toxic compounds that are naturally produced by certain types of moulds")
                                  )
    aflatoxin_name = models.CharField(max_length=127,
                                      null=True,
                                      blank=True,
                                      help_text=_("Name of poisonous carcinogens that are produced by certain molds")
                                      )
    aflatoxin_unit = models.CharField(max_length=127,
                                      null=True,
                                      blank=True,
                                      help_text=_("Unit of poisonous carcinogens that are produced by certain molds")
                                      )
    aflatoxin_value = models.CharField(max_length=127,
                                       null=True,
                                       blank=True,
                                       help_text=_("Value of poisonous carcinogens that are produced by certain molds")
                                       )
    temperature = models.IntegerField(null=True,
                                      blank=True,
                                      help_text=_("Temperature of environment where sample was kept.")
                                      )
    temperature_exposure_hours = models.CharField(max_length=127,
                                                  null=True,
                                                  blank=True,
                                                  help_text=_("How long sample was on certain temperature in hours")
                                                  )
    microbiological_id = models.CharField(max_length=127,
                                          null=True,
                                          blank=True,
                                          help_text=_("ID of microbiological sample.")
                                          )
    microbiological_unit = models.CharField(max_length=127,
                                            null=True,
                                            blank=True,
                                            help_text=_("Unit used to estimate the number of viable bacteria "
                                                        "or fungal cells in a sample.")
                                            )
    microbiological_value = models.CharField(max_length=127,
                                             null=True,
                                             blank=True,
                                             help_text=_("Number of viable bacteria or fungal cells in a sample.")
                                             )
    other_species = models.CharField(max_length=127,
                                     null=True,
                                     blank=True,
                                     help_text=_("Other species that can be in sample.")
                                     )

    adulteration_id = models.CharField(max_length=127,
                                       null=True,
                                       blank=True,
                                       help_text=_("ID of test for fake sample.")
                                       )
    alcohol_label = models.CharField(max_length=127,
                                     null=True,
                                     blank=True,
                                     help_text=_("Type of alcohol that is tested.")
                                     )
    authentic = models.CharField(max_length=127,
                                 null=True,
                                 blank=True,
                                 help_text=_("Is tested alcohol authentic or not.")
                                 )
    purity_smp = models.CharField(max_length=127,
                                  null=True,
                                  blank=True,
                                  help_text=_("Additional parameter for food adulteration.")
                                  )
    low_value_filler = models.CharField(max_length=127,
                                        null=True,
                                        blank=True,
                                        help_text=_("Additional parameter for food adulteration.")
                                        )
    nitrogen_enhancer = models.CharField(max_length=127,
                                         null=True,
                                         blank=True,
                                         help_text=_("Additional parameter for food adulteration.")
                                         )
    hazard_one_name = models.CharField(max_length=127,
                                       null=True,
                                       blank=True,
                                       help_text=_("Additional parameter for food adulteration.")
                                       )
    hazard_one_pct = models.CharField(max_length=127,
                                      null=True,
                                      blank=True,
                                      help_text=_("Additional parameter for food adulteration.")
                                      )
    hazard_two_name = models.CharField(max_length=127,
                                       null=True,
                                       blank=True,
                                       help_text=_("Additional parameter for food adulteration.")
                                       )
    hazard_two_pct = models.CharField(max_length=127,
                                      null=True,
                                      blank=True,
                                      help_text=_("Additional parameter for food adulteration.")
                                      )
    diluted_pct = models.CharField(max_length=127,
                                   null=True,
                                   blank=True,
                                   help_text=_("Additional parameter for food adulteration.")
                                   )
    package = models.CharField(max_length=127,
                               null=True,
                               blank=True,
                               help_text=_("Additional parameter for food adulteration.")
                               )
    adulterated = models.CharField(max_length=127,
                                   null=True,
                                   blank=True,
                                   help_text=_("Check if sample is adulterated or not")
                                   )
    configuration = JSONField(null=True,
                              blank=True,
                              help_text=_("Configuration of phasma device.")
                              )
    vis = JSONField(null=True,
                    blank=True,
                    help_text=_("Visible spectrometer data.")
                    )
    nir = JSONField(null=True,
                    blank=True,
                    help_text=_("Near-infrared spectrometer data.")
                    )
    fluo = JSONField(null=True,
                     blank=True,
                     help_text=_("Fluorescence spectrometer data.")
                     )
    white_reference_time = models.CharField(max_length=127,
                                            null=True,
                                            blank=True,
                                            help_text=_("Time of white reference measurement.")
                                            )
    date_created = models.DateTimeField(_('date created'),
                                        default=timezone.now,
                                        help_text=_("Date when measurement was made.")
                                        )
    date_updated = models.DateTimeField(_('date updated'),
                                        auto_now=True,
                                        help_text=_("Date when measurement was updated.")
                                        )

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return str(self.sample_id)
