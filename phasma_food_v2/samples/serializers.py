from rest_framework import serializers


class RowSerializer(serializers.Serializer):
    """Mongo DB query for single document."""
    query = serializers.JSONField()
    db = serializers.CharField(max_length=254, required=False)
    collection = serializers.CharField(max_length=254)
    project = serializers.BooleanField()


class RowsSerializer(serializers.Serializer):
    """Mongo DB query for documents."""
    query = serializers.JSONField()
    db = serializers.CharField(max_length=254, required=False)
    collection = serializers.CharField(max_length=254)
    project = serializers.BooleanField()
