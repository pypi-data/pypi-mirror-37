import re
from rest_framework.pagination import PageNumberPagination

from .base import ReadOnlyTokenAuthedViewSet
from fakenews.models import FactCheck
from fakenews.serializers import (
    FactCheckSerializer,
    FactCheckFeedSerializer,
    FactCheckArticleSerializer,
    FactCheckSlugsSerializer,
)


class FactCheckPagination(PageNumberPagination):
    page_size = 4


class FactCheckViewset(ReadOnlyTokenAuthedViewSet):
    lookup_field = "slug"
    throttle_classes = []
    pagination_class = FactCheckPagination

    def get_serializer_class(self):
        if self.request.query_params.get("feed-type") == "slugs-only":
            return FactCheckSlugsSerializer
        if self.request.query_params.get("feed-type") == "article":
            return FactCheckArticleSerializer
        if hasattr(self, "action") and self.action == "list":
            return FactCheckFeedSerializer
        return FactCheckSerializer

    def get_queryset(self):
        queryset = (
            FactCheck.objects.all()
            .select_related(
                "claim_reviewed",
                "claim_reviewed__disinformation_type",
                "author",
            )
            .prefetch_related("claim_reviewed__tags")
        )

        # Filter Author First Name
        author_first = self.request.query_params.get("fname", "")
        author_first_parts = re.split(r"\s+|\|", author_first)
        if author_first != "":
            queryset = queryset.filter(
                author__first_name__in=author_first_parts
            )

        # Filter Author Last Name
        author_last = self.request.query_params.get("lname", "")
        author_last_parts = re.split(r"\s+|\|", author_last)
        if author_last != "":
            queryset = queryset.filter(author__last_name__in=author_last_parts)

        # Filter Type
        type = self.request.query_params.get("type", "")
        types = type.split("|")
        if type != "":
            queryset = queryset.filter(
                claim_reviewed__disinformation_type__label__in=types
            )

        # Filter Status
        status = self.request.query_params.get("status", "")
        statuses = status.split("|")
        if status != "":
            queryset = queryset.filter(status__in=statuses)

        # Filter Tags
        tag = self.request.query_params.get("tag", "")
        tags = tag.split("|")
        if tag != "":
            queryset = queryset.filter(claim_reviewed__tags__name__in=tags)

        # Remove duplicates and order by date published and date_modified
        queryset = queryset.distinct().order_by(
            "-publish_date", "-date_modified"
        )

        return queryset
