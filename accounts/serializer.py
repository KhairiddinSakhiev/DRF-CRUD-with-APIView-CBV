from .models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ("username", "password", "confirm_password", "email")
    
    def validate(self, data):
        password = data.get("password")
        confirm = data.pop("confirm_password")
        if password != confirm:
            raise serializers.ValidationError("Passwords do not match! Please try again")
        return super().validate(data)
    
    def create(self, validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name")
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only = True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only = True)
        
        