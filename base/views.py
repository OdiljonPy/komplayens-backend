from .models import (
    Region, District, FAQ,
    AboutUs, CorruptionRisk, CorruptionCase
)
from .serializers import (
    RegionSerializer, DistrictSerializer,
    FAQSerializer, AboutUsSerializer,
    CorruptionRiskSerializer, CorruptionCaseSerializer
)
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


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

    @swagger_auto_schema(
        operation_summary='Details of Region',
        operation_description='Details of Region',
        responses={200: RegionSerializer()},
        tags=['Region']
    )
    def detail_(self, request, pk=None):
        region = Region.objects.filter(id=pk).first()
        if region is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Region not found')
        serializer = RegionSerializer(region, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class DistrictViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Districts',
        operation_description='List of Districts',
        responses={200: DistrictSerializer(many=True)},
        tags=['District']
    )
    def list(self, request):
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Details of District',
        operation_description='Details of District',
        responses={200: DistrictSerializer()},
        tags=['District']
    )
    def detail_(self, request, pk=None):
        district = District.objects.filter(id=pk).first()
        if district is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='District not found')
        serializer = DistrictSerializer(district, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class FAQViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of FAQs',
        operation_description='List of FAQs',
        responses={200: FAQSerializer(many=True)},
        tags=['FAQ']
    )
    def list(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Details of FAQ',
        operation_description='Details of FAQ',
        responses={200: FAQSerializer()},
        tags=['FAQ']
    )
    def detail_(self, request, pk=None):
        faq = FAQ.objects.filter(id=pk).first()
        if faq is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='FAQ not found')
        serializer = FAQSerializer(faq, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class AboutUsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Get last About Us',
        operation_description='Get last About Us',
        responses={200: AboutUsSerializer()},
        tags=['AboutUs']
    )
    def last(self, request):
        about_us = AboutUs.objects.order_by('-created_at').first()
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
