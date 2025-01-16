from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .utils import phone_number_validation
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'organization', 'first_name', 'last_name', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        if 'password' in self.validated_data:
            self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    organization = serializers.ReadOnlyField(source='organization.id')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    role = serializers.IntegerField()


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[phone_number_validation])
    password = serializers.CharField(required=True)


class PasswordRecoverySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[phone_number_validation])
