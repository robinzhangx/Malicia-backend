from datetime import datetime
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from fitting.redis_store import redis_store
from ft_accounts.models import User
from ft_accounts.serializers import UserSerializer
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

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        if 'user' in request.DATA:
            user_id = int(request.DATA.get('user'))
            if user_id == request.user.id:
                return Response({
                    'code': 4000,
                    'message': 'Not able to follow self'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                target = User.objects.get(id=user_id)
                follow, created = Follow.objects.get_or_create(left=request.user, right=target)
                if created:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    timestamp = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
                    redis_store.zadd('followers_{0}'.format(request.user.id), timestamp, user_id)
                    return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist, _:
                return Response({
                    'code': 4001,
                    'message': 'User does not exists'
                }, status=status.HTTP_400_BAD_REQUEST)


class FollowingUser(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request, user_id):
        user = request.user
        rank = redis_store.zrank('followers_{0}'.format(user.id), user_id)
        return Response({
            "following": rank is not None
        })

    def delete(self, request, user_id):
        user = request.user
        redis_store.zrem('followers_{0}'.format(user.id), user_id)
        Follow.objects.filter(left=user, right__id=user_id).delete()
        return Response(status=status.HTTP_200_OK)
