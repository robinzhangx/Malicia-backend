from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('ft_accounts.urls')),
    url(r'^api/images/(?P<filename>.*)$', 'ft_media.views.upload_view'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
