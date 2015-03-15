from django.conf.urls import patterns, url
from ft_accounts.views import UserExists, Register, Logout, Login, Me, WeixinBind

urlpatterns = patterns(
    '',
    url('api/accounts/user_exists/', UserExists.as_view()),
    url('api/accounts/register', Register.as_view()),
    url('api/accounts/logout', Logout.as_view()),
    url('api/accounts/login', Login.as_view()),
    url('api/accounts/me', Me.as_view()),
    url('api/accounts/bind/weixin', WeixinBind.as_view())

)