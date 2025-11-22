from rest_framework import generics, permissions, views, response, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from .models import *


class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    

class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            return response.Response({
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)
        return response.Response("Invalid credentials!", status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenSerializer
    def post(self, request, *args, **kwargs):
        token = request.data.get("refresh")
        if token:
            try:
                refresh_token = RefreshToken(token)
                return response.Response({
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token)
                }, status=status.HTTP_200_OK)
            except Exception as err:
                return response.Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return response.Response("Token must be set", status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        token = request.data.get("token")
        if token:
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return response.Response("User logged out!", status=status.HTTP_205_RESET_CONTENT)
        return response.Response("You must set refresh token to logged out user", status=status.HTTP_400_BAD_REQUEST)

    