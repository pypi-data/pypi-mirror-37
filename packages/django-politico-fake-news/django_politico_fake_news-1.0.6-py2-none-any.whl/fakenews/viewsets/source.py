from .base import TokenAuthedViewSet

from fakenews.models import Source
from fakenews.serializers import SourceSerializer, SourceListSerializer


class SourceViewset(TokenAuthedViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    lookup_field = 'pk'
    pagination_class = None
    throttle_classes = []

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return SourceListSerializer
        return SourceSerializer
