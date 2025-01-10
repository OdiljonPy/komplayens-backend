from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import (
    CategoryOrganization, Organization, Training,
    ElectronLibraryCategory, TrainingCategory,
    ElectronLibrary, News, HonestyTest,
    ConflictAlert, Profession, ProfessionalEthics,
    OfficerAdvice, ReportType, NewsCategory,
    HonestyTestCategory, HonestyTestStatistic,
    HonestyTestResult,
)

from .serializers import (
    CategoryOrganizationSerializer, OrganizationSerializer,
    TrainingSerializer, TrainingDetailSerializer, TrainingCategorySerializer,
    ElectronLibraryCategorySerializer, ElectronLibrarySerializer, NewsSerializer,
    ProfessionSerializer, ProfessionalEthicsSerializer, OfficerAdviceSerializer,
    ReportTypeSerializer, ViolationReportSerializer, TechnicalSupportSerializer,
    ConflictAlertSerializer, ConflictAlertTypeSerializer, TrainingParamValidator,
    ParamValidateSerializer, NewsParamValidator, NewsCategorySerializer,
    NewsDetailSerializer, ProfessionalEthicsParamValidator, OfficerAdviceParamValidator,
    HonestyTestCategorySerializer, HonestyTestResultSerializer,
    HonestyTestResultRequestSerializer, HonestyTestResultStatisticSerializer,
    HonestyParamSerializer, HonestyTestSerializer, HonestyTestSendResultSerializer
)
from .utils import file_one_create, file_two_create, file_three_create, calculate_percent
from .repository.training_paginator import training_paginator
from .repository.organization_paginator import get_paginated_organizations
from .repository.news_paginator import news_paginator
from .repository.electron_library_paginator import get_paginated_e_library
from .repository.profession_paginator import profession_paginator
from .repository.officer_advice_paginator import officer_advice_paginator
from authentication.utils import create_customer


class OrganizationViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Page number"),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Page size"),
            openapi.Parameter(name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Category id"),
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Search term"),
        ],
        operation_summary='Organization List',
        operation_description='List of all organizations',
        responses={200: OrganizationSerializer(many=True)},
        tags=['Organization']
    )
    def organization_list(self, request):
        param_serializer = ParamValidateSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=param_serializer.errors)
        category_id = param_serializer.validated_data.get('category_id')
        filter_ = Q()
        if category_id:
            filter_ |= Q(category_id=category_id)
        if request.query_params.get('q'):
            filter_ |= Q(name__icontains=request.query_params.get('q'))
        organizations = Organization.objects.filter(filter_)
        response = get_paginated_organizations(request_data=organizations, context={'request': request},
                                               page=param_serializer.validated_data.get('page'),
                                               page_size=param_serializer.validated_data.get('page_size')
                                               )
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Organization Categories',
        operation_description='List of all organization categories',
        responses={200: CategoryOrganizationSerializer()},
        tags=['Organization']
    )
    def organization_categories(self, request):
        data = CategoryOrganization.objects.all()
        serializer = CategoryOrganizationSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class TrainingViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Training list with filter',
        operation_description='List of all trainings with filter',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size number'),
            openapi.Parameter(
                name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='search parameter'),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='search parameter'),
        ],
        responses={200: TrainingSerializer()},
        tags=['Training']
    )
    def training_list(self, request):
        serializer = TrainingParamValidator(data=request.query_params)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        params = serializer.data
        filter_ = Q(name__icontains=params.get('q')) | Q(description__icontains=params.get('q'))
        if params.get('category_id'):
            filter_ &= Q(category_id=params.get('category_id'))
        data = Training.objects.filter(filter_, is_published=True)
        result = training_paginator(
            data, context={'request': request}, page=params.get('page'), page_size=params.get('page_size'))
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Training detail',
        operation_description='Training detail',
        responses={200: TrainingSerializer()},
        tags=['Training']
    )
    def training(self, request, pk):
        data = Training.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = TrainingDetailSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='List of all training categories',
        operation_description='List of all training categories',
        responses={200: TrainingSerializer()},
        tags=['Training']
    )
    def training_category(self, request):
        data = TrainingCategory.objects.all()
        serializer = TrainingCategorySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ElectronLibraryViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Page number"),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Page size"),
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Search term"),
            openapi.Parameter(name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Category id"),
        ],
        operation_summary='ElectronLibrary List',
        operation_description='List of electron libraries',
        responses={200: ElectronLibrarySerializer(many=True)},
        tags=['ElectronLibrary']
    )
    def electron_library_list(self, request):
        param_serializer = ParamValidateSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=param_serializer.errors)
        category_id = param_serializer.validated_data.get('category_id')
        filter_ = Q()
        if request.query_params.get('q'):
            filter_ |= Q(name__icontains=request.query_params.get('q'))
        if category_id:
            filter_ |= Q(category_id=category_id)
        data = ElectronLibrary.objects.filter(filter_, is_published=True)
        result = get_paginated_e_library(request_data=data, context={'request': request},
                                         page=param_serializer.validated_data.get('page'),
                                         page_size=param_serializer.validated_data.get('page_size'))
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary='ElectronLibrary Categories',
        operation_description='List of all electron library categories',
        responses={200: ElectronLibraryCategorySerializer(many=True)},
        tags=['ElectronLibrary']
    )
    def electron_library_category(self, request):
        data = ElectronLibraryCategory.objects.all()
        serializer = ElectronLibraryCategorySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class NewsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='News list with filters',
        operation_description='News list with filters',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page number'),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page_size number'),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='category id'),
            openapi.Parameter(
                name='popular', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='popularity parameter'),
            openapi.Parameter(
                name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='sort order')
        ],
        responses={200: NewsSerializer()},
        tags=['News']
    )
    def news_list(self, request):
        serializer = NewsParamValidator(data=request.query_params)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        params = serializer.data
        filter_ = Q()
        if params.get('category_id'):
            filter_ &= Q(category_id=params.get('category_id'))

        order_by = [
            {'new': '-created_at', 'old': 'created_at'}.get(params.get('order_by')),
        ]

        params.get('popular') and order_by.append('-view_count')

        data = News.objects.filter(filter_, is_published=True).order_by(*order_by)
        result = news_paginator(
            data, context={'request': request}, page=params.get('page'), page_size=params.get('page_size'))
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='News detail with pk',
        operation_description='News detail with pk',
        responses={200: NewsSerializer()},
        tags=['News']
    )
    def news(self, request, pk):
        data = News.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = NewsDetailSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='News category list',
        operation_description='News category list',
        responses={200: NewsCategorySerializer(many=True)},
        tags=['News']
    )
    def news_category(self, request):
        data = NewsCategory.objects.all()
        serializer = NewsCategorySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class HonestyViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Honesty test categories',
        operation_description='List of all honest test categories',
        responses={200: HonestyTestCategorySerializer(many=True)},
        tags=['HonestyTest']
    )
    def honesty_test_categories(self, request):
        data = HonestyTestCategory.objects.filter(in_term=True)
        serializer = HonestyTestCategorySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='organization_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Organization id'),
            openapi.Parameter(name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Category id'),
        ],
        operation_summary='Honesty tests by category id',
        operation_description='List of all honesty test by category id',
        responses={200: HonestyTestSerializer()},
        tags=['HonestyTest']
    )
    def honesty_test_list(self, request):
        customer = create_customer(request)
        query_params = HonestyParamSerializer(data=request.query_params)

        if not query_params.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=query_params.errors)

        category_id = query_params.validated_data.get('category_id')
        organization_id = query_params.validated_data.get('organization_id')
        test_stats = HonestyTestStatistic.objects.filter(
                test_type_id=category_id,
                organization_id=organization_id,
                customer_id=customer.id)
        test_result = HonestyTestResult.objects.filter(
                test__category_id=category_id,
                customer_id=customer.id)
        if test_stats and test_result:
            result_serializer = HonestyTestSendResultSerializer(test_result, many=True, context={'request': request})
            percent = calculate_percent(category_id=category_id, customer=customer)
            return Response(data={'new': False, 'percent': percent, 'result': result_serializer.data, 'ok': True}, status=status.HTTP_200_OK)
        stats_data = {'test_type' : category_id, 'organization': organization_id, 'customer': customer.id}

        stats_serializer = HonestyTestResultStatisticSerializer(data=stats_data, context={'request': request})
        if not stats_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=stats_serializer.errors)
        stats_serializer.save()

        questions = HonestyTest.objects.filter(category_id=category_id)
        serializer = HonestyTestSerializer(questions, many=True, context={'request': request})
        return Response(data={'new': True, 'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Honesty test Result',
        operation_description='Honesty test Result',
        request_body=HonestyTestResultRequestSerializer(many=True),
        responses={200: HonestyTestResultSerializer(many=True)},
        tags=['HonestyTest']
    )
    def honesty_test_result(self, request):
        serializer = HonestyTestResultSerializer(data=request.data, many=True, context={'request': request})

        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        question = serializer.validated_data[0].get('test')
        customer = create_customer(request)
        category_id = HonestyTest.objects.filter(id=question.id).first().category_id
        if (HonestyTestStatistic.objects.filter(
                test_type_id=category_id,
                customer_id=customer.id).exists() and
                HonestyTestResult.objects.filter(
                    test__category_id=category_id,
                    customer_id=customer.id).exists()
        ):
            raise CustomApiException(ErrorCodes.FORBIDDEN, message='You have already solved this test')

        serializer.save()
        category_id = HonestyTest.objects.filter(id=question.id).first().category_id
        percent = calculate_percent(category_id=category_id, customer=customer)
        return Response(data={'percent': percent, 'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ConflictAlertViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(
            name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Type of ConflictAlert'
        )],
        operation_summary='Conflict alert',
        operation_description='Create conflict alert',
        request_body=ConflictAlertSerializer,
        responses={200: ConflictAlertSerializer()},
        tags=['ConflictAlert']
    )
    def create_conflict_alert(self, request):
        param_serializer = ConflictAlertTypeSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=param_serializer.errors)
        file_type = param_serializer.validated_data.get('type')
        serializer = ConflictAlertSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        if file_type == 1:
            file_one_create(serialized_data=serializer.data)
        elif file_type == 2:
            file_two_create(serialized_data=serializer.data)
        elif file_type == 3:
            file_three_create(serialized_data=serializer.data)
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Conflict alert',
        operation_description='Detail of conflict alert',
        responses={200: ConflictAlertSerializer()},
        tags=['ConflictAlert']
    )
    def conflict_alert(self, request, pk):
        data = ConflictAlert.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ConflictAlertSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Conflict alert delete',
        operation_description='Delete conflict alert',
        responses={200: ConflictAlertSerializer()},
        tags=['ConflictAlert']
    )
    def delete_conflict_alert(self, request, pk):
        data = ConflictAlert.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.INVALID_INPUT)
        data.delete()
        return Response(data={'result': '', 'ok': True}, status=status.HTTP_200_OK)


class ProfessionalEthicsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List Professional Ethics',
        operation_description='List Professional Ethics',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(
                name='profession_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Profession ID'),
            openapi.Parameter(
                name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search param'),
        ],
        responses={200: ProfessionalEthicsSerializer()},
        tags=['ProfessionalEthics']
    )
    def professional_ethics_list(self, request):
        serializer = ProfessionalEthicsParamValidator(data=request.query_params)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        params = serializer.data
        filter_ = (
                Q(title__icontains=params.get('q'))
                | Q(description__icontains=params.get('q'))
                | Q(case__icontains=params.get('q'))
        )
        if params.get('profession_id'):
            filter_ &= Q(profession_id=params.get('profession_id'))
        data = ProfessionalEthics.objects.filter(filter_)
        result = profession_paginator(
            data, context={'request': request}, page=params.get('page'), page_size=params.get('page_size'))
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail Professional Ethics',
        operation_description='Detail Professional Ethics',
        responses={200: ProfessionalEthicsSerializer()},
        tags=['ProfessionalEthics']
    )
    def professional_ethics(self, request, pk):
        data = ProfessionalEthics.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ProfessionalEthicsSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Category Profession Ethics',
        operation_description='Category Profession Ethics',
        responses={200: ProfessionSerializer()},
        tags=['ProfessionalEthics']
    )
    def profession_list(self, request):
        data = Profession.objects.all()
        serializer = ProfessionSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class OfficerAdviceViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Officer Advices',
        operation_description='Create Officer Advices',
        request_body=OfficerAdviceSerializer(),
        responses={201: OfficerAdviceSerializer()},
        tags=['OfficerAdvice']
    )
    def create_officer_advice(self, request):
        data = request.data
        data.update({'officer': request.user.id})
        serializer = OfficerAdviceSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Get Officer Advices',
        operation_description='Get Officer Advices',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page number'),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page size number'),
            openapi.Parameter(
                name='professional_ethics', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Professional ethics id'),
        ],
        responses={200: OfficerAdviceSerializer()},
        tags=['OfficerAdvice']
    )
    def officer_advice_list(self, request):
        serializer = OfficerAdviceParamValidator(data=request.query_params)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        params = serializer.data
        data = OfficerAdvice.objects.filter(
            is_published=True, professional_ethics=params.get('professional_ethics')).order_by('created_at')
        result = officer_advice_paginator(
            data, context={'request': request}, page=params.get('page'), page_size=params.get('page_size')
        )
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)


class ViolationReportViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Violation Report',
        operation_description='Create Violation Reports',
        request_body=ViolationReportSerializer(),
        responses={201: ViolationReportSerializer()},
        tags=['ViolationReport']
    )
    def create_violation_report(self, request):
        serializer = ViolationReportSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Get Violation Reports type',
        operation_description='Get Violation Reports type',
        responses={200: ReportTypeSerializer()},
        tags=['ViolationReport']
    )
    def report_types(self, request):
        data = ReportType.objects.all()
        serializer = ReportTypeSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class TechnicalSupportViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Technical Support',
        operation_description='Send message to Technical Support',
        request_body=TechnicalSupportSerializer(),
        responses={201: TechnicalSupportSerializer()},
        tags=['TechnicalSupport']
    )
    def create_technical_support(self, request):
        serializer = TechnicalSupportSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)
