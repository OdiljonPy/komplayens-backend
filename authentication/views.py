from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .utils import gen_otp_code, create_otp, check_otp
from .models import User, OTP
from .serializers import (
    UserCreateSerializer, UserSerializer, UserLoginSerializer,
    OTPSerializer
)


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=UserCreateSerializer(),
        responses={201: UserCreateSerializer()},
        tags=["User"],
    )
    def create(self, request):
        data = request.data
        user = User.objects.filter(phone_number=data.get('phone_number')).first()
        if user:
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS)
        serializer = UserCreateSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user = serializer.save()
        otp_key = create_otp(user.id)
        return Response(data={'result': {'otp_key': otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=OTPSerializer(),
        responses={200: OTPSerializer()},
        tags=["User"],
    )
    def verify_otp(self, request):
        serializer = OTPSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        check_otp(serializer.data)

    @swagger_auto_schema(
        request_body=UserLoginSerializer(),
        responses={200: UserLoginSerializer()},
        tags=["User"],
    )
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user = User.objects.filter(phone_number=serializer.data.get('phone_number')).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)

        if not check_password(serializer.data.get('password'), user.password):
            raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)
        login_time = timezone.now()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role
        access_token['login_time'] = login_time.isoformat()
        user.login_time = login_time
        user.save()
        return Response(
            data={'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token)}, 'ok': True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserCreateSerializer(),
        responses={200: UserCreateSerializer()},
        tags=["User"],
    )
    def user_update(self, request):
        data = request.data
        if ('phone_number' in data and
                User.objects.filter(phone_number=data.get('phone_number').exclude(id=request.user.id).exists())):
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS)

        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        serializer = UserCreateSerializer(user, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        tags=["User"],
    )
    def user_detail(self, request):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = UserSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
