from rest_framework import serializers
from fakenews.models import DisinformationType


class DisinformationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisinformationType
        fields = '__all__'


class DisinformationTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisinformationType
        fields = (
            "pk",
            "label",
        )


class DisinformationTypeContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisinformationType
        fields = (
            "label",
            "description",
            "color_primary",
            "color_light"
        )
