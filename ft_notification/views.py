import json
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ft_notification.utils import create_notification, get_notifications, mark_notification, get_notification


class NotificationsAPIView(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request):
        user = request.user
        page = int(request.GET.get("page", 0))
        page_size = int(request.GET.get("page_size", 20))
        notifications = get_notifications(user.id, page=page, page_size=page_size)

        return Response({
            "notifications": [json.loads(n) for n in notifications]
        })


class MarkNotificationsAPIView(APIView):
    permission_classes = IsAuthenticated,

    def post(self, request, notification_id):
        user = request.user
        read = request.data['read']
        notification = mark_notification(user.id, notification_id, read=read)
        return Response(notification)
    def get(self, request, notification_id):
        user = request.user
        notification = get_notification(user.id, notification_id)
        return Response(notification)


class NotificationAdminAPIView(APIView):
    permission_classes = IsAdminUser,

    def post(self, request):
        obj = request.data
        user_id = obj['user_id']
        notification = obj['notification']
        create_notification(user_id, notification)
        return Response(status=201)
