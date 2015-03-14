from django.conf.urls import patterns, url
from ft_accounts.views import UserExists, Register, Logout

urlpatterns = patterns(
    '',
    url('api/accounts/user_exists/', UserExists.as_view()),
    url('api/accounts/register', Register.as_view()),
    url('api/accounts/logout', Logout.as_view()),
)