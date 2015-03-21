from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ft_social.models import Follow
from ft_social.serializers import FollowerSerializer, FollowingSerializer


class Follower(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(right=user)


class Following(ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(left=user)
