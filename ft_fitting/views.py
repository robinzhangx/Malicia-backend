from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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


class IngredientCRUD(APIView):
    permission_classes = ()
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get(self, request, fitting_id):
        qs = Ingredient.objects.filter(fittings__id=fitting_id)
        serializer = IngredientSerializer(qs, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=400)


class IngredientAPIView(IngredientCRUD):
    pass


class IngredientDetailView(IngredientCRUD):
    pass


class IngredientsForUser(APIView):
    def get(self, request, user_id):
        serializer = IngredientSerializer(Ingredient.objects.filter(user_id=user_id), many=True)
        return Response(serializer.data)


class FittingsForUser(APIView):
    def get(self, request, user_id):
        serializer = FittingSerializer(Fitting.objects.filter(user_id=user_id), many=True)
        return Response(serializer.data)


class IngredientAsks(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AskSerializer
    queryset = Ask.objects.all()

    def get(self, request, ingredient_id):
        queryset = self.queryset.filter(ingredient_id=ingredient_id)
        if queryset.exists():
            serializer = AskSerializer(queryset.all(), many=True, context={"request": request})
            return Response(data=serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, ingredient_id):
        serializer = AskSerializer(data=request.data, context={
            "request": request,
            "ingredient_id": ingredient_id,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientLike(APIView):
    def post(self, request, ingredient_id):
            like, created = LikeIngredient.objects.get_or_create(user=request.user, ingredient_id=ingredient_id)
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

    def delete(self, request, ingredient_id):
            LikeIngredient.objects.filter(user_id=request.user.id, ingredient_id=ingredient_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
