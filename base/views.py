from .models import (
    Region, District, FAQ,
    AboutUs, Banner, StatisticYear,
    RainbowStatistic, LinerStatistic,
    QuarterlyStatistic
)
from .serializers import (
    RegionSerializer, DistrictSerializer,
    FAQSerializer, AboutUsSerializer,
    TypeSerializer, AboutUsTypeSerializer,
    BannerSerializer, StatisticYearSerializer,
    RainbowStatisticSerializer, LinerStatisticSerializer,
    StatisticParamSerializer, QuarterlyStatisticSerializer
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
    def list(self, request, pk):
        districts = District.objects.filter(region_id=pk).select_related('region')
        serializer = DistrictSerializer(districts, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class FAQViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of FAQs',
        operation_description='List of FAQs',
        manual_parameters=[
            openapi.Parameter(name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
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
            openapi.Parameter(
                name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description="About US Type, choices: 1-'About Conflict of Interest' "
                            "2-'About Corruption Risk' 3-'About Promotion and Useful Information'"),],
        responses={200: AboutUsSerializer()},
        tags=['AboutUs']
    )
    def last(self, request):
        param_serializer = AboutUsTypeSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, param_serializer.errors)
        about_us_type = param_serializer.validated_data.get('type')
        about_us = AboutUs.objects.filter(type=about_us_type, is_published=True).order_by('-created_at').first()
        if not about_us:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='This type of About Us not Found')
        serializer = AboutUsSerializer(about_us, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class BannerViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Banner list',
        operation_description='List of Banners',
        responses={200: BannerSerializer(many=True)},
        tags=['Banner']
    )
    def banner_list(self, request):
        banners = Banner.objects.filter(is_published=True)[:3]
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class StatisticsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Statistic Year',
        operation_description='Get Statistic Year',
        responses={200: StatisticYearSerializer(many=True)},
        tags=['Statistics']
    )
    def statistic_year(self, request):
        statistic_year = StatisticYear.objects.all()
        serializer = StatisticYearSerializer(statistic_year, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='year_id', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER, description='Statistics Year ID'),
        ],
        operation_summary='Rainbow and Liner Statistics by year id',
        operation_description='Get Rainbow and Liner Statistics by year id',
        responses={200: RainbowStatisticSerializer()},
        tags=['Statistics']
    )
    def statistics(self, request):
        param_serializer = StatisticParamSerializer(data=request.query_params, context={'request': request})

        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, param_serializer.errors)
        year_id = param_serializer.validated_data.get('year_id')
        if not year_id:
            year = StatisticYear.objects.order_by('-year').first()
            year_id = getattr(year, 'id', None)
        if not year_id:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Statistic Year does not exist')

        rainbow_statistics = RainbowStatistic.objects.filter(year_id=year_id).first()
        if not rainbow_statistics:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Rainbow statistic not found')
        liner_statistics = LinerStatistic.objects.filter(year_id=year_id).order_by('-percentage')
        if not liner_statistics:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Liner statistic not found')

        rainbow_serializer = RainbowStatisticSerializer(rainbow_statistics, context={'request': request})
        liner_serializer = LinerStatisticSerializer(liner_statistics, many=True, context={'request': request})
        return Response(
            data={'result': {'rainbow' : rainbow_serializer.data, 'liner': liner_serializer.data},'ok': True},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='year_id', in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER, description='Statistics Year ID'),
        ],
        operation_summary='Quarterly Statistics by year id',
        operation_description='Get Quarterly Statistics by year id',
        responses={200: QuarterlyStatisticSerializer(many=True)},
        tags=['Statistics']
    )
    def quarterly_statistics(self, request):
        param_serializer = StatisticParamSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, param_serializer.errors)
        year_id = param_serializer.validated_data.get('year_id')
        if not year_id:
            year = StatisticYear.objects.order_by('-year').first()
            year_id = getattr(year, 'id', None)
        if not year_id:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Statistic Year does not exist')
        quarterly_statistics = QuarterlyStatistic.objects.filter(year_id=year_id).order_by('-this_year')
        if not quarterly_statistics:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Quarterly statistic not found in this year')
        serializer = QuarterlyStatisticSerializer(quarterly_statistics, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
