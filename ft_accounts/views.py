from pprint import pprint
import datetime
from django.contrib.auth import logout
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ft_accounts.models import WeixinAccount, User
from ft_accounts.serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer, \
    serialize_user_with_token


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
            if User.objects.filter(username=nickname).exists():
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

                user = User(nickname=nickname, email=email)
                user.set_password(password)
                user.save()
                return Response(serialize_user_with_token(user, with_token=True), status=201)
            except IntegrityError, e:
                error_message = e.message
                if error_message.find('username') != -1:
                    error_code = 4001
                    error_message = 'nickname already taken'
                elif error_message.find('email') != -1:
                    error_code = 4002
                    error_message = 'email already taken'
                else:
                    error_code = 4003

                return Response({
                    "code": error_code,
                    "message": error_message,
                }, status=409)
        else:
            return Response(serializer.errors, status=400)


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(serialize_user_with_token(user, with_token=True), status=201)
        else:
            return Response(serializer.errors, status=400)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        logout(request)
        # Do some clean up logic
        return Response(status=200)


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)


class WeixinBind(APIView):
    def post(self, request):
        try:
            obj = request.data

            access_token = obj['access_token']
            expires_in = int(obj['expires_in'])
            refresh_token = obj['refresh_token']
            union_id = obj['unionid']

            city = obj['city']
            country = obj['country']
            avatar_url = obj['headimgurl']
            language = obj['language']
            nickname = obj['nickname']
            openid = obj['openid']
            province = obj['province']
            sex = obj['sex']

            existing = WeixinAccount.objects.filter(union_id=union_id)
            if existing.exists():
                # TODO Also check the access token
                weixin = existing.first()
                return Response(serialize_user_with_token(weixin.user, with_token=True), status=200)

            weixin = WeixinAccount()
            weixin.access_token = access_token
            weixin.expires_in = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
            weixin.refresh_token = refresh_token
            weixin.union_id = union_id
            weixin.open_id = openid

            weixin.city = city
            weixin.province = province
            weixin.country = country
            weixin.avatar = avatar_url
            weixin.language = language
            weixin.nickname = nickname
            weixin.sex = sex

            weixin.save()  # Save first

            # TODO Check that we have the correct access_token, if no, we return to client that the id is not valid

            # If it is valid
            # Then we check whether the user already logged in, if yes, then we bind the weixin to the user
            # Else, we create a new user, with no usable password, then before user sets password manually, he can only
            # login by weixin

            if request.user.is_authenticated():
                weixin.user = request.user
                # If user don't have avatar yet, use the weixin
                if weixin.user.avatar is None:
                    weixin.user.avatar = weixin.avatar
                    weixin.user.save()
                weixin.save()
                return Response(status=200)
            else:
                # Create a new user, try to use the nickname if not applicable, then we append some random chars
                user = User(nickname=nickname)
                user.set_unusable_password()
                user.save()

                weixin.user = user
                weixin.save()

                user.gender = User.Gender_Male if weixin.male() else User.Gender_Female
                user.save()

                return Response(serialize_user_with_token(user, with_token=True), status=201)

        except Exception, e:
            pprint(e)
            return Response(status=400)



