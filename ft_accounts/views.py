from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


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
