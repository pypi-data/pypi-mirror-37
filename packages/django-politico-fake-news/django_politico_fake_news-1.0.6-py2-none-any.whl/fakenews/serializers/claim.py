from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from fakenews.models import Claim
from .share import ShareSerializer, ShareFeedSerializer
from .disinformation_type import DisinformationTypeContextSerializer


class ClaimSerializer(TaggitSerializer, serializers.ModelSerializer):
    disinformation_type = serializers.SerializerMethodField()
    share_set = ShareSerializer(many=True, read_only=True)
    tags = TagListSerializerField(read_only=True)

    def get_disinformation_type(self, obj):
        return obj.disinformation_type.pk

    class Meta:
        model = Claim
        fields = (
            "disinformation_type",
            "short_text",
            "canoncial_url",
            "archive_url",
            "share_set",
            "tags"
        )


class ClaimFeedSerializer(TaggitSerializer, serializers.ModelSerializer):
    share_set = ShareFeedSerializer(many=True, read_only=True)
    tags = TagListSerializerField(read_only=True)

    class Meta:
        model = Claim
        fields = (
            "short_text",
            "canoncial_url",
            "share_set",
            "tags"
        )


class ClaimArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    disinformation_type = DisinformationTypeContextSerializer()
    share_set = ShareFeedSerializer(many=True, read_only=True)
    tags = TagListSerializerField(read_only=True)

    class Meta:
        model = Claim
        fields = (
            "short_text",
            "disinformation_type",
            "share_set",
            "tags"
        )
