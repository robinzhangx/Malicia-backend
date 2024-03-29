from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('ft_accounts.urls')),
    url(r'', include('ft_fitting.urls')),
    url(r'', include('ft_notification.urls')),
    url(r'', include('ft_social.urls')),
    url(r'^api/images/(?P<filename>.*)$', 'ft_media.views.upload_view'),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
