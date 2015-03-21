from django.conf.urls import patterns, url
from ft_social.views import Follower

urlpatterns = patterns(
    '',
    url(r'^api/social/followers', Follower.as_view()),
    url(r'^api/social/following', Follower.as_view()),
)