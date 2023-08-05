from .base import TokenAuthedViewSet

from django.contrib.auth.models import User
from fakenews.serializers import UserSerializer, UserListSerializer


class UserViewset(TokenAuthedViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    pagination_class = None
    throttle_classes = []

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return UserListSerializer
        return UserSerializer
