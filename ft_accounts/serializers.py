# coding=utf-8
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from ft_accounts.models import User


class UserRegisterSerializer(serializers.Serializer):
    # TODO make sure nickname not contain @
    nickname = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)


class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=128, default=None)
    password = serializers.CharField(max_length=64)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if identifier.find('@') == -1:
            nickname = identifier
            email = None
        else:
            nickname = None
            email = identifier

        if identifier and password:
            user = authenticate(nickname=nickname, email=email, password=password)

            if user:
                if not user.is_active:
                    raise ValidationError(u'用户没有激活')
            else:
                raise ValidationError(u'无法使用提供的账号登录')
        else:
            raise ValidationError(u'请提供昵称或邮箱以及密码')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'date_joined', 'avatar', 'height', 'gender', 'weight', 'bmi')


def serialize_user_with_token(user, with_token=False):
    return_obj = UserSerializer(user).data

    if with_token:
        token, _ = Token.objects.get_or_create(user=user)
        return_obj.update({
            "token": token.key
        })
    return return_obj