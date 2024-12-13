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
from drf_yasg import openapi
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
    def detail(self, request, pk=None):
        region = Region.objects.filter(id=pk).first()
        if region is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Region not found')
        serializer = RegionSerializer(region, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a Region',
        operation_description='Create a Region',
        request_body=RegionSerializer(),
        responses={200: RegionSerializer()},
        tags=['Region']
    )
    def create(self, request):
        data = request.data
        serializer = RegionSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a Region',
        operation_description='Update a Region',
        request_body=RegionSerializer(),
        responses={200: RegionSerializer()},
        tags=['Region']
    )
    def update(self, request, pk=None):
        region = Region.objects.filter(id=pk).first()
        if region is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Region not found')
        serializer = RegionSerializer(region, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Delete a Region',
        operation_description='Delete a Region',
        tags=['Region']
    )
    def delete(self, request, pk=None):
        region = Region.objects.filter(id=pk).first()
        if region is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Region not found')
        region.delete()
        return Response(data={'result': '', 'ok': True}, status=status.HTTP_200_OK)


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
    def detail(self, request, pk=None):
        district = District.objects.filter(id=pk).first()
        if district is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='District not found')
        serializer = DistrictSerializer(district, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a District',
        operation_description='Create a District',
        request_body=DistrictSerializer(),
        responses={200: DistrictSerializer()},
        tags=['District']
    )
    def create(self, request):
        data = request.data
        serializer = DistrictSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a District',
        operation_description='Update a District',
        request_body=DistrictSerializer(),
        responses={200: DistrictSerializer()},
        tags=['District']
    )
    def update(self, request, pk=None):
        district = District.objects.filter(id=pk).first()
        if district is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='District not found')
        serializer = DistrictSerializer(district, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Delete a District',
        operation_description='Delete a District',
        tags=['District']
    )
    def delete(self, request, pk=None):
        district = District.objects.filter(id=pk).first()
        if district is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='District not found')
        district.delete()
        return Response(data={'result': '', 'ok': True}, status=status.HTTP_200_OK)


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
    def detail(self, request, pk=None):
        faq = FAQ.objects.filter(id=pk).first()
        if faq is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='FAQ not found')
        serializer = FAQSerializer(faq, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a FAQ',
        operation_description='Create a FAQ',
        request_body=FAQSerializer(),
        responses={200: FAQSerializer()},
        tags=['FAQ']
    )
    def create(self, request):
        data = request.data
        serializer = FAQSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a FAQ',
        operation_description='Update a FAQ',
        request_body=FAQSerializer(),
        responses={200: FAQSerializer()},
        tags=['FAQ']
    )
    def update(self, request, pk=None):
        faq = FAQ.objects.filter(id=pk).first()
        if faq is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='FAQ not found')
        serializer = FAQSerializer(faq, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Delete a FAQ',
        operation_description='Delete a FAQ',
        tags=['FAQ']
    )
    def delete(self, request, pk=None):
        faq = FAQ.objects.filter(id=pk).first()
        if faq is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='FAQ not found')
        faq.delete()
        return Response(data={'result': '', 'ok': True}, status=status.HTTP_200_OK)
