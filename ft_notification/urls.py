from django.conf.urls import patterns, url
from ft_notification.views import NotificationsAPIView, NotificationAdminAPIView

urlpatterns = patterns(
    '',
    url(r'^api/notifications', NotificationsAPIView.as_view()),
    url(r'^api/admin/notifications', NotificationAdminAPIView.as_view())
)