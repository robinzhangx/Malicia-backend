# coding=utf-8
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from ft_accounts.models import UserProfile


class UserRegisterSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)


class UserLoginSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=128, default=None)
    email = serializers.EmailField(default=None)
    password = serializers.CharField(max_length=64)

    def validate(self, attrs):
        nickname = attrs.get('nickname')
        email = attrs.get('email')
        password = attrs.get('password')

        if (nickname or email) and password:
            user = authenticate(username=nickname, email=email, password=password)

            if user:
                if not user.is_active:
                    raise ValidationError(u'用户没有激活')
            else:
                raise ValidationError(u'无法使用提供的账号登录')
        else:
            raise ValidationError(u'请提供昵称或邮箱以及密码')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        read_only_fields = ('nickname', 'height', 'weight', 'bmi')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'profile')


def serialize_user_with_token(user, with_token=False):
    return_obj = UserSerializer(user).data

    if with_token:
        token, _ = Token.objects.get_or_create(user=user)
        return_obj.update({
            "token": token.key
        })
    return return_obj