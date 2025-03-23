from users.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Django imports
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model


# Simple JWT imports
from rest_framework_simplejwt.tokens import RefreshToken




User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        required=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": _("Password fields didn't match.")}
            )

        return attrs
    

    def create(self, validate_data):
        user = User.objects.create_user(
            username= validate_data['username'],
            email= validate_data['email'],
            role=validate_data.get('role', 'nurse')
        )

        user.set_password(raw_password=validate_data['password'])
        user.save()
        return user