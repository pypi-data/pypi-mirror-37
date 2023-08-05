from rest_framework import serializers
from fakenews.models import Share
from .source import SourceSerializer


class ShareSerializer(serializers.ModelSerializer):
    source = SourceSerializer()

    class Meta:
        model = Share
        fields = (
            "pk",
            "order",
            "source",
            "url",
            "publish_date"
        )


class ShareFeedSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    def get_source(self, obj):
        return obj.source.name

    class Meta:
        model = Share
        fields = (
            "source",
            "url",
            "publish_date"
        )
