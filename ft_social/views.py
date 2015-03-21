from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ft_accounts.models import User
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
            user_id = request.DATA.get('user')
            follow, created = Follow.objects.get_or_create(left=request.user, right=User.objects.get(id=user_id))
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)


class FollowingUser(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request, user_id):
        user = request.user
        return Response({
            "following": Follow.objects.filter(left=user, right_id=user_id).exists()
        })
