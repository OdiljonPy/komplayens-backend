from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from .models import User, OTP
from .utils import (
    otp_create, otp_verification, is_user_created
)
from .serializers import (
    UserCreateSerializer, UserSerializer, UserLoginSerializer,
    OTPSerializer, ResendOTPSerializer
)


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=UserCreateSerializer(),
        responses={201: UserCreateSerializer()},
        tags=["User"],
    )
    def create(self, request):
        user = is_user_created(request)
        if user and user.is_verify:
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS)

        if user is not None:
            otp_key = otp_create(user.id)
            serializer = UserCreateSerializer(user, data=request.data, partial=True, context={'request': request})
            if not serializer.is_valid():
                raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
            serializer.save()
            return Response(data={'result': {'otp_key': otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user = serializer.save()

        otp_key = otp_create(user.id)
        return Response(data={'result': {'otp_key': otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=OTPSerializer(),
        responses={200: ''},
        tags=["User"],
    )
    def verify_otp(self, request):
        serializer = OTPSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user_id = otp_verification(serializer.data)
        User.objects.filter(id=user_id).update(is_verify=True)
        return Response(data={'result': 'Successfully verified', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ResendOTPSerializer(),
        responses={200: ResendOTPSerializer()},
        tags=["User"],
    )
    def resend_otp(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        otp = OTP.objects.filter(otp_key=serializer.data.get('otp_key')).first()
        if not otp:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP key is invalid')
        otp_key = otp_create(user_id=otp.user_id)
        return Response(data={'result': {'otp_key': otp_key}, 'ok': True}, status=status.HTTP_200_OK)

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

        if not user.is_verify:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='User is not verified')

        if not user.active:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='User is not active')

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
        request_body=UserCreateSerializer(),
        responses={200: UserCreateSerializer()},
        tags=["User"],
    )
    def user_update(self, request):
        if is_user_created(request):
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
        user = User.objects.filter(id=request.user.id, status=2, active=True).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = UserSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
