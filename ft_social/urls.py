from django.conf.urls import patterns, url
from ft_social.views import Follower, Following, FollowingUser


urlpatterns = patterns(
    '',
    url(r'^api/social/followers/$', Follower.as_view()),
    url(r'^api/social/following/$', Following.as_view()),
    url(r'^api/social/following/(?P<user_id>[^/.])/', FollowingUser.as_view()),
)