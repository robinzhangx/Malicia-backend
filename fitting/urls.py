from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'', include('ft_accounts.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
