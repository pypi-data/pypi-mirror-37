from .base import TokenAuthedViewSet

from fakenews.models import DisinformationType
from fakenews.serializers import (
    DisinformationTypeSerializer,
    DisinformationTypeListSerializer
)


class DisinformationTypeViewset(TokenAuthedViewSet):
    queryset = DisinformationType.objects.all()
    serializer_class = DisinformationTypeSerializer
    lookup_field = 'pk'
    pagination_class = None
    throttle_classes = []

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return DisinformationTypeListSerializer
        return DisinformationTypeSerializer
