from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from fitting.redis_store import redis_store

r = redis_store


class NotificationsAPIView(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request):
        user = request.user
        page = int(request.GET.get("page", 0))
        page_size = int(request.GET.get("page_size", 20))

        index = page * page_size
        return Response({
            "notifications": r.lrange('notifications_%s' % user.id, index, page_size)
        })


class NotificationAdminAPIView(APIView):
    permission_classes = IsAdminUser,

    def post(self, request):
        obj = request.data
        user_id = obj['user_id']
        notification = obj['notification']

        r.lpush('notifications_%s' % str(user_id), notification)
        return Response(status=201)
