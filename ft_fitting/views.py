from rest_framework.viewsets import ModelViewSet
from ft_fitting.models import Fitting
from ft_fitting.serializers import FittingSerializer


class FittingViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = FittingSerializer
    queryset = Fitting.objects.all()

    def get_queryset(self):
        qs = super(FittingViewSet, self).get_queryset()
        return qs