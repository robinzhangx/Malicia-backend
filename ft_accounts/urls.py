from django.conf.urls import patterns, url
from ft_accounts.views import UserExists

urlpatterns = patterns(
    '',
    url('api/user_exists/', UserExists.as_view()),
)