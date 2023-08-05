from rest_framework import serializers
from fakenews.models import FactCheck

from .claim import ClaimSerializer, ClaimFeedSerializer, ClaimArticleSerializer
from .user import UserSerializer
from .slate import SlateSerializer


class FactCheckSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    claim_reviewed = ClaimSerializer()
    author = UserSerializer()

    class Meta:
        model = FactCheck
        fields = "__all__"


class FactCheckFeedSerializer(serializers.ModelSerializer):
    claim_reviewed = ClaimFeedSerializer()
    author = serializers.SerializerMethodField()
    disinformation_type = serializers.SerializerMethodField()
    color_primary = serializers.SerializerMethodField()
    color_light = serializers.SerializerMethodField()

    def get_author(self, obj):
        return "{} {}".format(obj.author.first_name, obj.author.last_name)

    def get_disinformation_type(self, obj):
        return obj.claim_reviewed.disinformation_type.label

    def get_color_primary(self, obj):
        return obj.claim_reviewed.disinformation_type.color_primary

    def get_color_light(self, obj):
        return obj.claim_reviewed.disinformation_type.color_light

    class Meta:
        model = FactCheck
        fields = (
            "slug",
            "headline",
            "deck",
            "author",
            "cover",
            "publish_date",
            "disinformation_type",
            "color_primary",
            "color_light",
            "claim_reviewed",
        )


class FactCheckArticleSerializer(serializers.ModelSerializer):
    claim_reviewed = ClaimArticleSerializer()
    author = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    def get_author(self, obj):
        return "{} {}".format(obj.author.first_name, obj.author.last_name)

    def get_explanation(self, obj):
        s = SlateSerializer(obj.explanation)
        return s.render()

    class Meta:
        model = FactCheck
        fields = (
            "slug",
            "headline",
            "deck",
            "author",
            "cover",
            "publish_date",
            "claim_reviewed",
            "explanation",
        )


class FactCheckSlugsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheck
        fields = ("id", "slug",)
