from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from ft_fitting.views import FittingViewSet, IngredientAPIView, IngredientLike, IngredientDetailView, IngredientCRUD, IngredientAsks

non_nested_router = DefaultRouter()
non_nested_router.register(r'fittings', FittingViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(non_nested_router.urls)),

    url(r'^api/fittings/(?P<fitting_id>[0-9]+)/ingredients/', IngredientAPIView.as_view()),

    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/asks/', IngredientAsks.as_view()),
    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/like/', IngredientLike.as_view()),
    url(r'^api/ingredients/(?P<pk>[0-9]+)/', IngredientDetailView.as_view()),
    url(r'^api/ingredients/', IngredientCRUD.as_view()),
)