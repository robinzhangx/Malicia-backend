from rest_framework.serializers import Serializer
from ft_accounts.serializers import UserSerializer


class FollowerSerializer(Serializer):
    def to_representation(self, instance):
        return UserSerializer(instance.left).data


class FollowingSerializer(Serializer):
    def to_representation(self, instance):
        return UserSerializer(instance.right).data
