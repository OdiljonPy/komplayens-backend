from .models import (
    Region, District, FAQ,
    AboutUs, CorruptionRisk, CorruptionCase
)
from .serializers import (
    RegionSerializer, DistrictSerializer,
    FAQSerializer, AboutUsSerializer,
    CorruptionRiskSerializer, CorruptionCaseSerializer,
    TypeSerializer, AboutUsTypeSerializer
)
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegionViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Regions',
        operation_description='List of Regions',
        responses={200: RegionSerializer(many=True)},
        tags=['Region']
    )
    def list(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class DistrictViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Districts by Region ID',
        operation_description='List of Districts by Region ID',
        responses={200: DistrictSerializer(many=True)},
        tags=['District']
    )
    def list(self, request, pk=None):
        districts = District.objects.filter(region_id=pk).select_related('region')
        serializer = DistrictSerializer(districts, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class FAQViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of FAQs',
        operation_description='List of FAQs',
        manual_parameters=[
            openapi.Parameter(name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1,
                              description="FAQ Type, choices: 1, 2, 3"),],
        responses={200: FAQSerializer(many=True)},
        tags=['FAQ']
    )
    def list(self, request):
        param_serializer = TypeSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, param_serializer.errors)
        faq_type = param_serializer.validated_data.get('type')
        faqs = FAQ.objects.filter(type=faq_type).order_by('-created_at')
        serializer = FAQSerializer(faqs, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class AboutUsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Get last About Us',
        operation_description='Get last About Us',
        manual_parameters=[
            openapi.Parameter(name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1,
                              description="About US Type, choices: 1, 2, 3, 4"), ],
        responses={200: AboutUsSerializer()},
        tags=['AboutUs']
    )
    def last(self, request):
        param_serializer = AboutUsTypeSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, param_serializer.errors)
        about_us_type = param_serializer.validated_data.get('type')
        about_us = AboutUs.objects.filter(type=about_us_type).order_by('-created_at').first()
        serializer = AboutUsSerializer(about_us, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class CorruptionRiskViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Corruption Risk',
        operation_description='Corruption Risk List',
        responses={200: CorruptionRiskSerializer(many=True)},
        tags=['CorruptionRisk']
    )
    def list(self, request):
        corruption_risk = CorruptionRisk.objects.all()
        serializer = CorruptionRiskSerializer(corruption_risk, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Corruption Risk',
        operation_description='Corruption Risk Details',
        responses={200: CorruptionRiskSerializer()},
        tags=['CorruptionRisk']
    )
    def detail_(self, request, pk=None):
        corruption_risk = CorruptionRisk.objects.filter(id=pk).first()
        if corruption_risk is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='CorruptionRisk not found')
        serializer = CorruptionRiskSerializer(corruption_risk, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class CorruptionCaseViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Corruption Case',
        operation_description='Corruption Case List',
        responses={200: CorruptionCaseSerializer(many=True)},
        tags=['CorruptionCase']
    )
    def list(self, request):
        corruption_case = CorruptionCase.objects.all()
        serializer = CorruptionCaseSerializer(corruption_case, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Corruption Case',
        operation_description='Corruption Case Details',
        responses={200: CorruptionCaseSerializer()},
        tags=['CorruptionCase']
    )
    def detail_(self, request, pk=None):
        corruption_case = CorruptionCase.objects.filter(id=pk).first()
        if corruption_case is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Corruption Case not found')
        serializer = CorruptionCaseSerializer(corruption_case, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
