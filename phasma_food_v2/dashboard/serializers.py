from typing import Any

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from phasma_food_v2.measurements.models import Measurement


class ListMeasurementSerializer(serializers.Serializer):
    """Serializer for Measurement model where filed name are changed
    to follow Python and Java Script conventions.
    """
    sampleID = serializers.IntegerField(source="sample_id")
    userID = serializers.CharField(source="owner", required=True)
    mobileID = serializers.CharField(source="mobile", required=True)
    laboratory = serializers.CharField(allow_null=True)
    deviceID = serializers.CharField(source="phasma_device")
    foodType = serializers.CharField(source="food_type", allow_null=True)
    foodSubtype = serializers.CharField(source="food_subtype", allow_null=True)
    useCase = serializers.CharField(source="use_case", allow_null=True)
    UseCaseSampleID = serializers.CharField(source="use_case_sample_id", read_only=True)
    granularity = serializers.CharField(allow_null=True)
    mycotoxins = serializers.CharField(allow_null=True)
    aflatoxinName = serializers.CharField(source="aflatoxin_name", allow_null=True)
    aflatoxinUnit = serializers.CharField(source="aflatoxin_unit", allow_null=True)
    aflatoxinValue = serializers.CharField(source="aflatoxin_value", allow_null=True)
    temperature = serializers.CharField(allow_null=True)
    tempExposureHours = serializers.CharField(source="temperature_exposure_hours", allow_null=True)
    microbioSampleId = serializers.CharField(source="microbiological_id", allow_null=True)
    microbiologicalUnit = serializers.CharField(source="microbiological_unit", allow_null=True)
    microbiologicalValue = serializers.CharField(source="microbiological_value", allow_null=True)
    otherSpecies = serializers.CharField(source="other_species", allow_null=True)
    adulterationSampleId = serializers.CharField(source="adulteration_id", allow_null=True)
    alcoholLabel = serializers.CharField(source="alcohol_label", allow_null=True)
    authentic = serializers.CharField(allow_null=True)
    puritySMP = serializers.CharField(source="purity_smp", allow_null=True)
    lowValueFiller = serializers.CharField(source="low_value_filler", allow_null=True)
    nitrogenEnhancer = serializers.CharField(source="nitrogen_enhancer", allow_null=True)
    hazardOneName = serializers.CharField(source="hazard_one_name", allow_null=True)
    hazardOnePct = serializers.CharField(source="hazard_one_pct", allow_null=True)
    hazardTwoName = serializers.CharField(source="hazard_two_name", allow_null=True)
    hazardTwoPct = serializers.CharField(source="hazard_two_pct", allow_null=True)
    dilutedPct = serializers.CharField(source="diluted_pct", allow_null=True)
    package = serializers.CharField(allow_null=True)
    adul = serializers.CharField(source="adulterated", allow_null=True)
    whiteReferenceTime = serializers.CharField(source="white_reference_time", allow_null=True)
    dateTime = serializers.DateTimeField(source="date_created", read_only=True)
    dateUpdated = serializers.DateTimeField(source="date_updated", read_only=True)

    class Meta:
        model = Measurement
        fields = ["sampleID", "userID", "mobileID", "laboratory", "deviceID", "foodType", "foodSubtype", "useCase",
                  "UseCaseSampleID", "granularity", "mycotoxins", "aflatoxinName", "aflatoxinUnit", "aflatoxinValue",
                  "temperature", "tempExposureHours", "microbioSampleId", "microbiologicalUnit", "microbiologicalValue",
                  "otherSpecies", "adulterationSampleId", "alcoholLabel", "authentic", "puritySMP", "lowValueFiller",
                  "nitrogenEnhancer", "hazardOneName", "hazardOnePct", "hazardTwoName", "hazardTwoPct", "dilutedPct",
                  "package", "adul", "whiteReferenceTime", "dateTime", "dateUpdated"
                  ]

    def to_representation(self, instance: Measurement) -> Measurement:
        """Change format of datetime filed to
        human readable one.

        Parameter:
            instance (obj): Measurement object

        Returns:
            instance (obj): Measurement object with changed format of
            datetime filed
        """
        representation = super().to_representation(instance)
        representation['result'] = instance.result.data if hasattr(instance, "result") else None
        representation['dateTime'] = instance.date_created.strftime("%d %b %Y %H:%M")
        representation['dateUpdated'] = instance.date_updated.strftime("%d %b %Y %H:%M")

        return representation


class MeasurementDownloadSerializer(serializers.Serializer):
    """Measurements list to be downloaded and sent via email."""
    measurements = serializers.ListField(
        child=serializers.CharField(max_length=254)
    )


class MeasurementMongoSerializer(serializers.Serializer):
    """Measurements list to be saved to Mongo DB."""
    measurements = serializers.ListField(
        child=serializers.CharField(max_length=254)
    )
    db = serializers.CharField(max_length=254, required=False)
    collection = serializers.CharField(max_length=254)

    def validate(self, attrs: dict) -> Any:
        """Check if collection name is according
        to rules.

        Parameter:
            attrs (dict): Request fields from body

        Returns:
            attrs (dict): Request fields from body
        """
        collection = attrs["collection"]
        collection_use_case, collection_food_type, *other = collection.split("_")

        check_use_cases = Measurement.objects.order_by(
            "use_case"
        ).distinct(
            "use_case"
        ).values_list(
            "use_case",
            "food_type"
        )
        collections_names = ["_".join(name).replace(" ", "").lower() for name in check_use_cases]
        if len(collections_names) > 1:
            raise serializers.ValidationError(
                _('You have selected more than one use case and food type {} when one per push is allowed.').format(
                    check_use_cases
                )
            )

        collection_name_first_part = "_".join(
            [collection_use_case.replace(" ", ""), collection_food_type.replace(" ", "")]
        ).lower()

        if collection_name_first_part not in collections_names:
            raise serializers.ValidationError(
                _('Collection name from measurement and collection provided mismatch.')
            )

        return attrs
