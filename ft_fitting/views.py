from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from ft_fitting.models import Fitting, Ingredient, LikeFitting, LikeIngredient, Ask
from ft_fitting.serializers import FittingSerializer, IngredientSerializer, LikeFittingSerializer, \
    LikeIngredientSerializer, AskSerializer


class FittingViewSet(ModelViewSet):
    permission_classes = IsAuthenticated,
    serializer_class = FittingSerializer
    queryset = Fitting.objects.all()

    @list_route(permission_classes=[])
    def list(self, request, *args, **kwargs):
        return super(FittingViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=['get'], permission_classes=[])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})


class AskViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AskSerializer
    queryset = Ask.objects.all()


class IngredientViewSet(ModelViewSet, NestedViewSetMixin):
    permission_classes = ()
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    @list_route(methods=['get'])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})


class LikeFittingViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeFittingSerializer
    queryset = LikeFitting.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class LikeIngredientViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeIngredientSerializer
    queryset = LikeIngredient.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


