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
    identifier = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False, error_messages={
        'required': '40040 identifier required',
        'max_length': '40041 identifier exceed max length',
        'blank': '40042 identifier field not allow blank',
        'null': '40043 identifier field not allow null',
    })
    password = serializers.CharField(max_length=64, required=True, allow_blank=False, allow_null=False, error_messages={
        'required': '40050 password field required',
        'max_length': '40051 password exceed max length',
        'blank': '40052 password field not allow blank',
        'null': '40053 password field not allow null',
    })

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
                    raise ValidationError('4001 User not active')
            else:
                raise ValidationError('4002 Not able to login')
        else:
            raise ValidationError('4003 Require identifier and password')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'date_joined', 'avatar', 'height', 'gender', 'weight', 'bmi')
        read_only_fields = ('id', 'nickname', 'email', 'date_joined')


def serialize_user_with_token(user, with_token=False):
    return_obj = UserSerializer(user).data

    if with_token:
        token, _ = Token.objects.get_or_create(user=user)
        return_obj.update({
            "token": token.key
        })
    return return_obj