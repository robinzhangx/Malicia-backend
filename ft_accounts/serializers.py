from django.contrib.auth.models import User
from rest_framework import serializers
from ft_accounts.models import UserProfile


class UserRegisterSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        read_only_fields = ('nickname', 'height', 'weight', 'bmi')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'profile')