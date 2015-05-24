from django.conf.urls import patterns, include, url
from fitting.router_extended import DefaultRouter

from ft_fitting.views import FittingViewSet, IngredientAPIView, IngredientLike, AliasAPIView

non_nested_router = DefaultRouter()
non_nested_router.register(r'fittings', FittingViewSet)
non_nested_router.register(r'ingredients', IngredientAPIView)

urlpatterns = patterns(
    '',
    url(r'^api/fittings/(?P<fitting_id>[0-9]+)/ingredients',
        AliasAPIView.as_view(url="/api/ingredients/?fitting={fitting_id}")),
    url(r'^api/', include(non_nested_router.urls)),
    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/like/', IngredientLike.as_view()),
)