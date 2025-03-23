from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout,get_user_model

# Serializers
from users.serializer import UserLoginSerializer, RegisterSerializer

# Rest framework Imports
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

# Simple JWT imports
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()
# Helper functions


class UserLoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                token = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'email' : user.email,
                    'message': 'Successfully logged in',
                }, status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UserRegistrationView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({
                'refresh': str(token),
                'access': str(token.access_token),
                'email': user.email,
                'message': 'Successfully registered',
            }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogoutView(APIView):
    def post(self, request):
        refresh_token = request.data('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': f'User, {request.user.username} has logged out successfully'
            })
        return Response({
            'error_meesage' : 'Invalid token.'
        })