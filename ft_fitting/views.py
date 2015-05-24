# coding=utf-8
import urlparse

from django.core.urlresolvers import resolve
from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ft_accounts.models import User
from ft_fitting.models import Fitting, Ingredient, LikeFitting, LikeIngredient, Ask
from ft_fitting.serializers import FittingSerializer, IngredientSerializer, AskSerializer


class FittingViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = FittingSerializer
    queryset = Fitting.objects.prefetch_related('ingredients', 'likefitting_set').all()

    @list_route(permission_classes=[], url="{prefix}/")
    def list(self, request, *args, **kwargs):
        return super(FittingViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=['get'], permission_classes=[])
    def count(self, request):
        return Response({'count': self.get_queryset().count()})

    @detail_route(methods=['post', 'delete'], url='{prefix}/(?P<fitting_id>\d+)/like/')
    def like(self, request, fitting_id):
        if request.method.lower() == 'post':
            like, created = LikeFitting.objects.get_or_create(user=request.user, fitting_id=fitting_id)
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

        elif request.method.lower() == 'delete':
            LikeFitting.objects.filter(user_id=request.user.id, fitting_id=fitting_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class AliasAPIView(APIView):
    permission_classes = ()
    url = None

    def _handle(self, request, *args, **kwargs):
        target_url = self.url.format(**kwargs)
        parse_result = urlparse.urlparse(target_url)
        if parse_result.netloc == '':
            r = resolve(parse_result.path)
            if issubclass(r.func.cls, APIView):
                url_query_params = QueryDict(parse_result.query, mutable=True)
                url_query_params.update(request.GET)
                request._request.GET = url_query_params
                response = r.func(request)
                return response
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def get(self, request, *args, **kwargs):
        return self._handle(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._handle(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self._handle(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self._handle(request, *args, **kwargs)


class IngredientAPIView(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        qs = super(IngredientAPIView, self).get_queryset()
        if 'fitting' in self.request.GET:
            return qs.filter(fittings=self.request.GET['fitting'])
        return qs

    def create(self, request, *args, **kwargs):
        if 'fitting' in request.GET:
            request._request.POST["fitting"] = request.GET['fitting']
        return super(IngredientAPIView, self).create(request, *args, **kwargs)

    def list(self, request, **kwargs):
        """
        获取所有单品

        ---
        response_serializer: IngredientSerializer
        responseMessages:
            - code: 200
              message: OK
        """
        return super(IngredientAPIView, self).list(request, **kwargs)

    @list_route(methods=['get'], url='users/(?P<user_id>\d+)/ingredients/')
    def ingredients_for_user(self, request, user_id):
        """
        获取用户创建的所有单品

        ---
        response_serializer: IngredientSerializer
        parameters:
            - name: user_id
              description: Id of user
              required: true
              type: string
              paramType: path
        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: 用户不存在
        """
        user = get_object_or_404(User.objects.all(), id=user_id)
        qs = Ingredient.objects.filter(user=user)
        serializer = IngredientSerializer(qs, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url='ingredients/(?P<ingredient_id>\d+)/asks/')
    def asks(self, request, ingredient_id):
        """
        某一单品的询问

        ---
        response_serializer: AskSerializer

        """
        return Response(data=AskSerializer(Ask.objects.filter(ingredient_id=ingredient_id), many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url='ingredients/(?P<ingredient_id>\d+)/asks/')
    def create_ask(self, request, ingredient_id):
        """
        询问单品

        ---
        response_serializer: AskSerializer
        request_serializer: AskSerializer
        hide_parameters:
          - ingredient
        parameters:
          - name: Authorization
            message: Header for authentication
            type: string
            paramType: header
        """
        serializer = AskSerializer(data=request.data, context={
            "request": request,
            "ingredient_id": ingredient_id,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class FittingsForUser(APIView):
    def get(self, request, user_id):
        serializer = FittingSerializer(Fitting.objects.filter(user_id=user_id), many=True)
        return Response(serializer.data)


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
