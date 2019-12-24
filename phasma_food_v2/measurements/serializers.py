from typing import Union

from django.contrib.auth import get_user_model
from rest_framework import serializers
from fcm_django.models import FCMDevice
from phasma_food_v2.devices.models import PhasmaDevice

from .models import Measurement, Result, Image
from .utils import calculate_average
from .fields import Base64ImageField
from .tasks import measurement_rule_engine

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    camera = Base64ImageField(use_url=True, max_length=None, allow_null=True)
    name = serializers.CharField(max_length=254, required=True)

    class Meta:
        model = Image
        fields = "__all__"


class MeasurementSerializer(serializers.Serializer):
    """Measurement model where filed names are changed
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
    VIS = serializers.JSONField(source="vis", allow_null=True)
    NIR = serializers.JSONField(source="nir", allow_null=True)
    FLUO = serializers.JSONField(source="fluo", allow_null=True)
    camera = ImageSerializer(many=True, write_only=True, allow_null=True, required=False)
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
                  "package", "adul", "VIS", "NIR", "FLUO", "camera", "whiteReferenceTime", "dateTime", "dateUpdated"
                  ]

    def create(self, validated_data: dict) -> Measurement:
        """Save Measurement object to DB

        Parameter:
            validated_data (dict): Measurement data that is validated and ready

        Returns:
            instance (obj): Measurement object saved in DB
        """
        use_case = validated_data.get("use_case")
        operation = self.context.get("operation")
        validated_data = calculate_average(validated_data)
        validated_data = self.attach_use_case_sample_id(validated_data)
        camera_data = validated_data.pop("camera") if "camera" in validated_data else None
        measurement_saved = Measurement.objects.create(**validated_data)
        if camera_data:
            for camera in camera_data:
                Image.objects.create(
                    measurement=measurement_saved,
                    camera=camera.get("camera"),
                    name=camera.get("name")
                )

        if use_case.lower() != "test":
            if operation.lower() == "analyze":
                validated_data["owner"] = str(validated_data.get("owner", ""))
                validated_data["mobile"] = str(validated_data.get("mobile", ""))
                validated_data["phasma_device"] = str(validated_data.get("phasma_device", ""))
                measurement_rule_engine.delay(validated_data)

        return measurement_saved

    def update(self, instance: Measurement, validated_data: dict) -> Measurement:
        """Update Measurement object

        Parameter:
            instance (obj): Measurement object that is currently in DB
            validated_data (dict): Measurement data that is used
            to update current measurement object

        Returns:
            instance (obj): Measurement object saved in DB
        """
        validated_data = self.attach_use_case_sample_id(validated_data)
        instance.sample_id = validated_data.get('sample_id', instance.sample_id)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.phasma_device = validated_data.get('phasma_device', instance.phasma_device)
        instance.laboratory = validated_data.get('laboratory', instance.laboratory)
        instance.food_type = validated_data.get('food_type', instance.food_type)
        instance.food_subtype = validated_data.get('food_subtype', instance.food_subtype)
        instance.use_case = validated_data.get('use_case', instance.use_case)
        instance.use_case_sample_id = validated_data.get("use_case_sample_id", instance.use_case_sample_id)
        instance.granularity = validated_data.get('granularity', instance.granularity)
        instance.mycotoxins = validated_data.get('mycotoxins', instance.mycotoxins)
        instance.aflatoxin_name = validated_data.get('aflatoxin_name', instance.aflatoxin_name)
        instance.aflatoxin_unit = validated_data.get('aflatoxin_unit', instance.aflatoxin_unit)
        instance.aflatoxin_value = validated_data.get('aflatoxin_value', instance.aflatoxin_value)
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.temperature_exposure_hours = validated_data.get('temperature_exposure_hours',
                                                                 instance.temperature_exposure_hours)
        instance.microbiological_id = validated_data.get('microbiological_id', instance.microbiological_id)
        instance.microbiological_unit = validated_data.get('microbiological_unit', instance.microbiological_unit)
        instance.microbiological_value = validated_data.get('microbiological_value', instance.microbiological_value)
        instance.other_species = validated_data.get('other_species', instance.other_species)
        instance.adulteration_id = validated_data.get('adulteration_id', instance.adulteration_id)
        instance.alcohol_label = validated_data.get('alcohol_label', instance.alcohol_label)
        instance.authentic = validated_data.get('authentic', instance.authentic)
        instance.purity_smp = validated_data.get('purity_smp', instance.purity_smp)
        instance.low_value_filler = validated_data.get('low_value_filler', instance.low_value_filler)
        instance.nitrogen_enhancer = validated_data.get('nitrogen_enhancer', instance.nitrogen_enhancer)
        instance.hazard_one_name = validated_data.get('hazard_one_name', instance.hazard_one_name)
        instance.hazard_one_pct = validated_data.get('hazard_one_pct', instance.hazard_one_pct)
        instance.hazard_two_name = validated_data.get('hazard_two_name', instance.hazard_two_name)
        instance.hazard_two_pct = validated_data.get('hazard_two_pct', instance.hazard_two_pct)
        instance.diluted_pct = validated_data.get('diluted_pct', instance.diluted_pct)
        instance.package = validated_data.get('package', instance.package)
        instance.adulterated = validated_data.get('adulterated', instance.adulterated)
        instance.configuration = validated_data.get('configuration', instance.configuration)
        instance.vis = validated_data.get('vis', instance.vis)
        instance.nir = validated_data.get('nir', instance.nir)
        instance.fluo = validated_data.get('fluo', instance.fluo)
        instance.fluo = validated_data.get('fluo', instance.fluo)
        instance.white_reference_time = validated_data.get('white_reference_time', instance.white_reference_time)
        camera_data = validated_data.pop("camera") if "camera" in validated_data else None
        Image.objects.filter(measurement=instance).delete()
        if camera_data:
            for camera in camera_data:
                Image.objects.create(measurement=instance,
                                     camera=camera.get("camera"),
                                     name=camera.get("name")
                                     )
        return instance

    def to_representation(self, instance: Measurement) -> dict:
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
        request = self.context.get('request')
        representation['camera'] = [{"name": m.name, "camera": request.build_absolute_uri(m.camera.url)} for m in
                                    Image.objects.filter(measurement_id=representation["sampleID"]).all()]
        return representation

    def validate_sampleID(self, attr: int) -> Union[serializers.ValidationError, int]:
        """Checks if measurement with ID already exists.

        Parameter:
            attr (str): Measurement ID

        Returns:
            attr (str): Measurement ID or raise error
        """
        request = self.context["request"]
        if request.method.lower() == "post":
            if Measurement.objects.filter(sample_id=attr).exists():
                raise serializers.ValidationError("Sample with ID [{}] already exists.".format(attr))
        return attr

    def validate_userID(self, attr: str) -> Union[serializers.ValidationError, User]:
        """Checks if user with ID exists.

        Parameter:
            attr (str): User ID

        Returns:
            attr (str): User instance or raise error
        """
        user_db = User.objects.filter(email=attr)
        user_db = user_db.first()
        if not user_db:
            raise serializers.ValidationError("User with email [{}] does not exist.".format(attr))

        user_req = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user_req = request.user
        if str(user_db.email) != str(user_req):
            raise serializers.ValidationError("User can only create/update/delete his measurement.")

        return user_db

    def validate_mobileID(self, attr: str) -> Union[serializers.ValidationError, FCMDevice]:
        """Checks if mobile with ID exists.

        Parameter:
            attr (str): Mobile ID

        Returns:
            attr (str): Mobile instance or raise error
        """
        mobile = FCMDevice.objects.filter(device_id=attr)
        if not mobile.exists():
            raise serializers.ValidationError("Mobile with #ID [{}] does not exist.".format(attr))

        return mobile.first()

    def validate_deviceID(self, attr: str) -> Union[serializers.ValidationError, PhasmaDevice]:
        """Checks if phasma device with ID exists.

        Parameter:
            attr (str): Phasma device ID

        Returns:
            attr (str): Phasma device instance or raise error
        """
        phasma_device = PhasmaDevice.objects.filter(mac=attr)
        if not phasma_device.exists():
            raise serializers.ValidationError("Phasma device with MAC address [{}] does not exist.".format(attr))

        return phasma_device.first()


    @staticmethod
    def attach_use_case_sample_id(data: dict) -> dict:
        """Update phasma device that user did measurement with.

        Parameter:
            data (dict): Measurement object

        Returns:
            data (dict): Measurement object
        """
        use_case = data.get("use_case")
        if use_case.lower() == "mycotoxins detection":
            data["use_case_sample_id"] = "{}_{}".format(data.get("aflatoxin_value"), data.get("aflatoxin_name"))
        elif use_case.lower() == "food spoilage":
            data["use_case_sample_id"] = data.get("microbiological_id")
        elif use_case.lower() == "food spoilage":
            data["use_case_sample_id"] = data.get("adulteration_id")
        else:
            data["use_case_sample_id"] = None

        return data


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for Result model."""

    class Meta:
        model = Result
        fields = "__all__"
