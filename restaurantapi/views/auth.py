from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Auth(ViewSet):

    permission_classes=[AllowAny]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        user = User.objects.create_user(first_name=request.data.get('first_name'), last_name=request.data.get('last_name'),email=request.data.get('email'), username=request.data.get('username'), password=request.data.get('password'))
        Token.objects.update_or_create(user=user)
        token = Token.objects.get(user=user)
        if token:
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
