from django.contrib import admin

from .models import Measurement, Result, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("measurement", 'camera', 'name')


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("sample_id", "owner", "mobile", "phasma_device",
                    "laboratory", "use_case", "use_case_sample_id", "food_type", "date_created")
    list_filter = ("food_type", "use_case")

    fieldsets = (
        ("Measurement", {"fields": ("sample_id", "owner", "mobile", "phasma_device")}),
        ("Sample Data", {"fields": ("laboratory", "use_case", "use_case_sample_id", "food_type", "food_subtype",
                                    "granularity", "mycotoxins", "aflatoxin_name", "aflatoxin_unit",
                                    "aflatoxin_value", "temperature", "temperature_exposure_hours",
                                    "microbiological_id", "microbiological_unit", "microbiological_value",
                                    "other_species", "adulteration_id", "alcohol_label", "authentic", "purity_smp",
                                    "low_value_filler", "nitrogen_enhancer", "hazard_one_name", "hazard_one_pct",
                                    "hazard_two_name", "hazard_two_pct", "diluted_pct", "package", "adulterated"
                                    )}),
        ("Configuration", {"fields": ("configuration",)}),
        ("Date created", {"fields": ("date_created", "date_updated", "white_reference_time")}),
    )
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("measurement", "data", "date_created")
    fieldsets = (
        ("Result", {"fields": ("measurement", "data")}),
        ("Date created", {"fields": ("date_created",)})
    )
    readonly_fields = ("date_created",)
    ordering = ("-date_created",)
