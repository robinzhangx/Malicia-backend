from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from ft_fitting.views import FittingViewSet, IngredientViewSet, LikeFittingViewSet, LikeIngredientViewSet, AskViewSet
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

(
    router.register(r'ingredients', IngredientViewSet)
          .register(r'asks', AskViewSet, base_name='asks', parents_query_lookups=['ingredient'])
)
router.register(r'like/fittings', LikeFittingViewSet)
router.register(r'like/ingredients', LikeIngredientViewSet)
router.register(r'asks', AskViewSet)

router.include_root_view = False

non_nested_router = DefaultRouter()
non_nested_router.register(r'fittings', FittingViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(non_nested_router.urls)),
)