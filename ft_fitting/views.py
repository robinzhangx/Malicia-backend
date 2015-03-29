from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from ft_fitting.models import Fitting, Ingredient, LikeFitting, LikeIngredient, Ask
from ft_fitting.serializers import FittingSerializer, IngredientSerializer, AskSerializer


class FittingViewSet(ModelViewSet):
    permission_classes = IsAuthenticated,
    serializer_class = FittingSerializer
    queryset = Fitting.objects.prefetch_related('ingredients', 'likefitting_set').all()

    @list_route(permission_classes=[])
    def list(self, request, *args, **kwargs):
        return super(FittingViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=['get'], permission_classes=[])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})

    @detail_route(methods=['post', 'delete'])
    def like(self, request, pk=None):
        if request.method.lower() == 'post':
            like, created = LikeFitting.objects.get_or_create(user=request.user, fitting_id=pk)
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

        elif request.method.lower() == 'delete':
            LikeFitting.objects.filter(user_id=request.user.id, fitting_id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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

    @detail_route(methods=['post', 'delete'])
    def like(self, request, pk=None):
        if request.method.lower() == 'post':
            like, created = LikeIngredient.objects.get_or_create(user=request.user, ingredient_id=pk)
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

        elif request.method.lower() == 'delete':
            LikeIngredient.objects.filter(user_id=request.user.id, ingredient_id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
