from pprint import pprint
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ft_accounts.serializers import UserRegisterSerializer, UserSerializer


class UserExists(APIView):
    def get(self, request):
        if 'email' in request.GET:
            email = request.GET['email']
            if User.objects.filter(email=email).exists():
                return Response({
                    'existing': True
                })

        elif 'nickname' in request.GET:
            nickname = request.GET['nickname']
            if User.objects.filter(profile__nickname=nickname).exists():
                return Response({
                    'existing': True
                })

        return Response({
            'existing': False
        })


class Register(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                nickname = serializer.validated_data.get('nickname')
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                user = User(username=nickname, email=email)
                user.set_password(password)
                user.save()

                user.profile.nickname = nickname
                user.profile.save()

                # return the created user
                user_serializer = UserSerializer(user)
                result = user_serializer.data
                token, _ = Token.objects.get_or_create(user=user)
                result.update({
                    "token": token.key
                })
                return Response(result, status=201)
            except IntegrityError, e:
                return Response({
                    "message": e.message
                }, status=409)
        else:
            return Response(serializer.errors, status=400)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        logout(request)
        # Do some clean up logic
        return Response(status=200)
