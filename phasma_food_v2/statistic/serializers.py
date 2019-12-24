from rest_framework import serializers
from .models import PlatformStatistic


class PlatformStatisticSerializer(serializers.ModelSerializer):
    """Serializer for platform statistic."""

    class Meta:
        model = PlatformStatistic
        fields = '__all__'
