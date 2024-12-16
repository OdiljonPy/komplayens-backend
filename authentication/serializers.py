from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .utils import phone_number_validation
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'phone_number', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        print('save called')
        if 'password' in self.validated_data:
            self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)

    def validate(self, attrs):
        if 'phone_number' in attrs:
            phone_number_validation(attrs.get('phone_number'))
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'role')


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class OTPSerializer(serializers.Serializer):
    otp_key = serializers.IntegerField(required=True)
    otp_code = serializers.UUIDField(required=True)
