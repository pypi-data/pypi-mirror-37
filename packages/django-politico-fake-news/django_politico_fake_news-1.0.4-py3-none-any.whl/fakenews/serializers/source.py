from rest_framework import serializers
from fakenews.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "pk",
            "name",
            "url",
            "description",
        )


class SourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "pk",
            "name",
        )
