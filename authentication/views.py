from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from .models import User
from .utils import (
    is_user_created, send_password_sms
)

from .serializers import (
    UserCreateSerializer, UserSerializer,
    UserLoginSerializer, PasswordRecoverySerializer,
    UserPasswordUpdateSerializer
)


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='User create',
        operation_description='Create a new user',
        request_body=UserCreateSerializer(),
        responses={201: UserCreateSerializer()},
        tags=["User"],
    )
    def create(self, request):
        user = is_user_created(request)
        if user:
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS)
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': 'User Created Successfully', 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Login',
        operation_description='Login a user',
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

        if user.is_active == 2:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Is User blocked')

        if user.role == 3 and user.status in (1, 3):
            message = {
                1: 'This user is being viewed',
                3: 'This user has been canceled'
            }.get(user.status)
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message=message)

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
        operation_summary='User update',
        operation_description='Update a user',
        request_body=UserPasswordUpdateSerializer(),
        responses={200: UserCreateSerializer()},
        tags=["User"],
    )
    def user_update(self, request):
        serializer = UserPasswordUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user = User.objects.filter(id=request.user.id, is_active=True).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)

        serializer = UserCreateSerializer(
            user, data=serializer.validated_data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='User details',
        operation_description='Details about a user',
        responses={200: UserSerializer()},
        tags=["User"],
    )
    def user_detail(self, request):
        user = User.objects.filter(id=request.user.id, status=2, is_active=True).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = UserSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Password recovery',
        operation_description='Recover a password',
        request_body=PasswordRecoverySerializer(),
        tags=["User"],
    )
    def password_recovery(self, request):
        serializer = PasswordRecoverySerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        phone_number = serializer.validated_data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        if user.is_active == 2:
            raise CustomApiException(ErrorCodes.USER_BLOCKED)
        new_password = send_password_sms(user)
        user.password = make_password(new_password)
        user.save(update_fields=['password'])
        return Response(data={'result': 'Password sent', 'ok': True}, status=status.HTTP_200_OK)
