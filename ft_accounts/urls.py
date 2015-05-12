from django.conf.urls import patterns, url
from ft_accounts.views import UserExists, Register, Logout, Login, Me, WeixinBind
from ft_fitting.views import IngredientsForUser, FittingsForUser

urlpatterns = patterns(
    '',
    url('^api/accounts/user_exists/', UserExists.as_view()),
    url('^api/accounts/register', Register.as_view()),
    url('^api/accounts/logout', Logout.as_view()),
    url('^api/accounts/login', Login.as_view()),
    url('^api/accounts/me', Me.as_view()),
    url('^api/accounts/bind/weixin', WeixinBind.as_view()),

    url(r'^api/users/(?P<user_id>[0-9]+)/ingredients/', IngredientsForUser.as_view()),
    url(r'^api/users/(?P<user_id>[0-9]+)/fittings/', FittingsForUser.as_view()),
)