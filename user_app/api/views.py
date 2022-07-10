from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api import serializers
from user_app import models

# so that we don't accidentally optimise and remove models
models


@api_view(['POST', ])
@permission_classes([AllowAny])
def registration_view(request):

    if request.method == 'POST':
        serializer = serializers.RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            # token, create = Token.objects.get_or_create(user=account)

            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = Token.objects.get(user=account).key

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("Logged out successfully", status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
def registration_view_jwt(request):

    if request.method == 'POST':
        serializer = serializers.RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email

            # generating jwt token
            refresh = RefreshToken.for_user(user=account)

            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
