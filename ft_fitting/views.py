from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ft_fitting.models import Fitting, Ingredient, FittingForDiscover
from ft_fitting.serializers import FittingSerializer, IngredientSerializer


class FittingViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = FittingSerializer
    queryset = Fitting.objects.all()

    @list_route(methods=['get'])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})

    @list_route(methods=['get'])
    def discover(self, request):
        prev_discover_id = int(request.GET.get('last_discover_id', 0))
        qs = FittingForDiscover.objects.filter(id__gt=prev_discover_id).order_by('id')
        if qs.exists():
            discover = qs[0]
            return_obj = self.serializer_class(discover.fitting).data
            return_obj.update({
                "discover_id": discover.id
            })
            return Response(return_obj)
        else:
            return Response({
                "code": 4000,
                "message": "Nothing left"
            }, status=400)


class IngredientViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    @list_route(methods=['get'])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})
