from typing import Union

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import PhasmaDevice

User = get_user_model()


class PhasmaDeviceSerializer(serializers.Serializer):
    """Serializer for Phasma device model."""

    mac = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def create(self, validated_data: dict) -> PhasmaDevice:
        """Save Phasma device to DB

        Parameter:
            validated_data (dict): Phasma device data that is validated and ready

        Returns:
            instance (obj): Phasma device object saved in DB
        """
        request = self.context["request"]
        phasma_device = PhasmaDevice(**validated_data)
        phasma_device._user = request.user
        phasma_device.save()
        return phasma_device

    def update(self, instance: PhasmaDevice, validated_data: dict) -> PhasmaDevice:
        """Update Phasma device object

        Parameter:
            instance (obj): Phasma device object that is currently in DB
            validated_data (dict): Phasma device data that is used
            to update current Phasma device object

        Returns:
            instance (obj): Measurement object saved in DB
        """
        request = self.context["request"]
        instance.mac = validated_data.get('mac', instance.mac)
        instance.name = validated_data.get('name', instance.name)
        instance._user = request.user
        instance.save()

        return instance

    def to_representation(self, instance: PhasmaDevice) -> PhasmaDevice:
        """Change format of datetime filed to
        human readable one.

        Parameter:
            instance (obj): Phasma device object

        Returns:
            instance (obj): Phasma device object with changed format of
            datetime filed
        """
        representation = super().to_representation(instance)
        representation['date_added'] = instance.date_added.strftime("%d %b %Y %H:%M")
        representation['date_updated'] = instance.date_updated.strftime("%d %b %Y %H:%M")

        return representation

    def validate_mac(self, attr: str) -> Union[serializers.ValidationError, str]:
        """Checks if phasma device with ID already exists.

        Parameter:
            attr (str): Phasm device ID

        Returns:
            attr (str): Phasma device ID or raise error
        """
        request = self.context["request"]
        if request.method.lower() == "post":
            if PhasmaDevice.objects.filter(mac=attr).exists():
                raise serializers.ValidationError("Phasma device with ID [{}] already exists.".format(attr))
        return attr
