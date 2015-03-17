from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from ft_fitting.views import FittingViewSet

router = DefaultRouter()
router.register('fittings', FittingViewSet)

router.include_root_view = False

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)