from datetime import datetime
from django.db.models import F
from django.utils import timezone
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
    HonestyTestCategory, ViolationReport,
    HonestyTestResult, CorruptionRisk,
    AnnouncementCategory, Announcement,
    CorruptionRiskMedia
)
from authentication.models import ContentViewer

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
    HonestyParamSerializer, HonestyTestSerializer, ViolationFileSerializer,
    GuiltyPersonSerializer, ViolationReportCreateSerializer,
    HonestyTestDefaultSerializer, CorruptionRiskSerializer,
    CorruptionRiskParamValidator, AnnouncementCategorySerializer,
    AnnouncementSerializer, CorruptionRiskMediaSerializer
)
from .repository.training_paginator import training_paginator
from .repository.organization_paginator import get_paginated_organizations
from .repository.news_paginator import news_paginator
from .repository.electron_library_paginator import get_paginated_e_library
from .repository.profession_paginator import profession_paginator
from .repository.officer_advice_paginator import officer_advice_paginator
from .repository.corruption_risk_paginator import corruption_risk_paginator
from .repository.announcement_paginator import get_paginated_announcement
from authentication.utils import create_customer
from .utils import (
    file_one_create, file_two_create, file_three_create,
    get_google_sheet_statistics, calculate_percent
)


class OrganizationViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Page number"),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Page size number"),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Category id"),
            openapi.Parameter(
                name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search term"),
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
            filter_ &= Q(category_id=category_id)
        if request.query_params.get('q'):
            filter_ &= Q(name__icontains=request.query_params.get('q'))
        organizations = Organization.objects.filter(filter_)
        response = get_paginated_organizations(
            request_data=organizations, context={'request': request}, page=param_serializer.validated_data.get('page'),
            page_size=param_serializer.validated_data.get('page_size')
        )
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Organization Categories',
        operation_description='List of all organization categories',
        manual_parameters=[
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search term"),
        ],
        responses={200: CategoryOrganizationSerializer()},
        tags=['Organization']
    )
    def organization_categories(self, request):
        search_param = request.query_params.get('q') or ''
        data = CategoryOrganization.objects.filter(name__icontains=search_param)
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
                name='from_date', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='From-date parameter'),
            openapi.Parameter(
                name='to_date', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='To-date parameter'),
            openapi.Parameter(
                name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search parameter'),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description='Category id parameter'),
            openapi.Parameter(
                name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                description="Order parameter {'new' or 'old'}"),
            openapi.Parameter(
                name='popular', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                description='Popular parameter. Default false')
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

        if params.get('from_date'):
            filter_ &= Q(created_at__gte=params.get('from_date'))

        if params.get('to_date'):
            filter_ &= Q(created_at__lte=params.get('to_date'))

        if params.get('category_id'):
            filter_ &= Q(category_id=params.get('category_id'))

        order_by = [
            {'new': '-created_at', 'old': 'created_at'}.get('order_by'),
        ]

        if params.get('popular') is not None:
            order_by.append('-view_count')

        data = Training.objects.filter(filter_, is_published=True).order_by(*order_by)
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
        data = Training.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        today = timezone.now().date()
        customer = create_customer(request)
        content_viewer = ContentViewer.objects.filter(content_id=pk, customer=customer, content_type=3).first()
        if not content_viewer:
            ContentViewer.objects.create(content_id=pk, customer=customer, content_type=3, view_day=today)
            data.views += 1
            data.save(update_fields=['views'])
        elif content_viewer.view_day < today:
            ContentViewer.objects.update(content_id=pk, customer=customer, content_type=3, view_day=today)
            data.views += 1
            data.save(update_fields=['views'])
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
        operation_summary='ElectronLibrary List',
        operation_description='List of electron libraries',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description="Page number (integer field)"),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description="Page size number (integer field)"),
            openapi.Parameter(
                name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                description="Search term (string field)"),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description="Category id (integer field)"),
        ],
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
            filter_ &= Q(name__icontains=request.query_params.get('q'))
        if category_id:
            filter_ &= Q(category_id=category_id)
        data = ElectronLibrary.objects.filter(filter_, is_published=True)
        result = get_paginated_e_library(
            request_data=data, context={'request': request}, page=param_serializer.validated_data.get('page'),
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
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Category id'),
            openapi.Parameter(
                name='popular', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='Popularity parameter'),
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

        order_by = []
        params.get('popular') and order_by.append('-view_count')
        order_by.append(
            {'new': '-created_at', 'old': 'created_at'}.get(params.get('order_by'))
        )

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
        data = News.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        today = timezone.now().date()
        customer = create_customer(request)
        content_viewer = ContentViewer.objects.filter(content_id=pk, customer=customer, content_type=2).first()

        if not content_viewer:
            ContentViewer.objects.create(content_id=pk, customer=customer, content_type=2, view_day=today)
            data.views += 1
            data.save(update_fields=['views'])

        elif content_viewer.view_day < today:
            ContentViewer.objects.update(content_id=pk, customer=customer, content_type=2, view_day=today)
            data.views += 1
            data.save(update_fields=['views'])
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
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Category id'),
        ],
        operation_summary='Honesty tests by category id',
        operation_description='List of all honesty test by category id',
        responses={200: HonestyTestSerializer()},
        tags=['HonestyTest']
    )
    def honesty_test_list(self, request):
        query_params = HonestyParamSerializer(data=request.query_params)
        customer = create_customer(request)
        if not query_params.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=query_params.errors)

        category_id = query_params.validated_data.get('category_id')

        if HonestyTestResult.objects.filter(test__category_id=category_id, customer_id=customer.id).exists():
            data = HonestyTest.objects.filter(category_id=category_id)
            result_serializer = HonestyTestSerializer(data, many=True, context={'customer': customer})
            percent = calculate_percent(category_id=category_id, customer=customer)
            return Response(data={'new': False, 'percent': percent, 'result': result_serializer.data, 'ok': True},
                            status=status.HTTP_200_OK)

        questions = HonestyTest.objects.filter(category_id=category_id)
        serializer = HonestyTestDefaultSerializer(questions, many=True, context={'customer': customer})
        return Response(data={'new': True, 'percent': None, 'result': serializer.data, 'ok': True},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='organization_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Organization id'),
            openapi.Parameter(
                name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Category id'),
        ],
        operation_summary='Honesty test Result',
        operation_description='Honesty test Result',
        request_body=HonestyTestResultRequestSerializer(many=True),
        responses={200: HonestyTestResultSerializer(many=True)},
        tags=['HonestyTest']
    )
    def honesty_test_result(self, request):
        customer = create_customer(request)
        query_params = HonestyParamSerializer(data=request.query_params)
        if not query_params.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=query_params.errors)
        category_id = query_params.validated_data.get('category_id')
        organization_id = query_params.validated_data.get('organization_id')

        if HonestyTestResult.objects.filter(test__category_id=category_id, customer_id=customer.id).exists():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='You have already solved this test')

        serializer = HonestyTestResultSerializer(data=request.data, many=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()

        stats_data = {'test_type': category_id, 'organization': organization_id, 'customer': customer.id}
        stats_serializer = HonestyTestResultStatisticSerializer(data=stats_data, context={'request': request})
        if not stats_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=stats_serializer.errors)
        stats_serializer.save()
        percent = calculate_percent(category_id=category_id, customer=customer)
        questions = HonestyTest.objects.filter(category_id=category_id)
        question_serializer = HonestyTestSerializer(questions, many=True, context={'customer': customer})
        return Response(data={'new': False, 'percent': percent, 'result': question_serializer.data, 'ok': True},
                        status=status.HTTP_200_OK)


class ConflictAlertViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(
            name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Type of ConflictAlert (1, 2, 3)'
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
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size number'),
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
        return Response(data={'result': result, 'comment_count': len(data), 'ok': True}, status=status.HTTP_200_OK)


class ViolationReportViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Violation Report',
        operation_description='Create Violation Report',
        request_body=ViolationReportCreateSerializer(),
        responses={201: ViolationReportSerializer()},
        tags=['ViolationReport']
    )
    def create_violation_report(self, request):
        serializer = ViolationReportSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        if not serializer.validated_data.get('is_anonim'):
            validated_data = serializer.validated_data
            if not (validated_data.get('informant_full_name') and validated_data.get('informant_phone_number') and
                    validated_data.get('informant_email')):
                raise CustomApiException(
                    ErrorCodes.VALIDATION_FAILED, message='Informant full name and phone and email are required')
        violation = serializer.save()

        files_data = []
        for file in request.FILES.getlist('file'):
            files_data.append({'report': violation.id, 'file': file})

        file_serializer = ViolationFileSerializer(data=files_data, many=True, context={'request': request})
        if not file_serializer.is_valid():
            ViolationReport.objects.filter(id=violation.id).delete()
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=file_serializer.errors)

        guilty_data = []
        full_names = request.data.getlist('full_name')
        positions = request.data.getlist('position')
        phone_numbers = request.data.getlist('phone_number')
        if len(full_names) != len(phone_numbers) or len(full_names) != len(positions):
            ViolationReport.objects.filter(id=violation.id).delete()
            raise CustomApiException(
                ErrorCodes.VALIDATION_FAILED, message='There is an error in the contact information.')

        for full_name in request.data.getlist('full_name'):
            guilty_data.append(
                {'report': violation.id,
                 'full_name': full_name,
                 'phone_number': phone_numbers.pop(0),
                 'position': positions.pop(0)
                 })

        guilty_person_serializer = GuiltyPersonSerializer(data=guilty_data, many=True, context={'request': request})
        if not guilty_person_serializer.is_valid():
            ViolationReport.objects.filter(id=violation.id).delete()
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=guilty_person_serializer.errors)

        file_serializer.save()
        guilty_person_serializer.save()

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


class CorruptionRiskViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Corruption Risk list api with filter',
        operation_description='Corruption Rist list api with filter',
        manual_parameters=[
            openapi.Parameter(
                name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(
                name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size'),
            openapi.Parameter(
                name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Page order (new or old)'),
            openapi.Parameter(
                name='status', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='CorruptionRisk status'),
            openapi.Parameter(
                name='from_date', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='From date'),
            openapi.Parameter(
                name='to_date', in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='To date'),
        ],
        tags=['CorruptionRisk']
    )
    def corruption_list(self, request):
        serializer = CorruptionRiskParamValidator(data=request.query_params)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        objects = CorruptionRisk.objects.filter(end_date__lte=datetime.today(), status=1)
        for result in objects:
            sheet_id = result.excel_url.split("/d/")[1].split("/")[0]
            result.result = get_google_sheet_statistics(sheets_id=sheet_id)
            result.status = 2
            result.save(update_fields=['result', 'status'])

        filter_ = Q()
        params = serializer.validated_data
        if params.get('status'):
            filter_ &= Q(status=params.get('status'))

        if params.get('from_date'):
            filter_ &= Q(start_date__lte=params.get('from_date'))

        if params.get('to_date'):
            filter_ &= Q(end_date__gte=params.get('to_date'))

        order_by = [
            {'new': '-created_at', 'old': '-created_at'}.get(params.get('order_by')),
        ]

        query_response = CorruptionRisk.objects.filter(filter_).order_by(*order_by)
        result = corruption_risk_paginator(
            query_response, page=params.get('page'), page_size=params.get('page_size'), context={'request': request})
        return Response(data={'result': result, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Corruption Risk detail api',
        operation_description='Corruption Risk detail api',
        tags=['CorruptionRisk']
    )
    def corruption_detail(self, request, pk):
        result = CorruptionRisk.objects.filter(id=pk).first()
        if not result:
            raise CustomApiException(ErrorCodes.NOT_FOUND)

        if not result.result:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='No response to the survey was created.')
        serializer = CorruptionRiskSerializer(result, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Corruption Risk Media list api',
        operation_description='Corruption Risk Media list api',
        tags=['CorruptionRisk']
    )
    def corruption_risk_media(self, request):
        file_list = CorruptionRiskMedia.objects.all()
        serializer = CorruptionRiskMediaSerializer(file_list, many=True, context={'request': request})
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


class AnnouncementViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Announcement Category',
        operation_description='Category of Announcement',
        responses={200: AnnouncementCategorySerializer(many=True)},
        tags=['Announcement']
    )
    def announcement_categories(self, request):
        categories = AnnouncementCategory.objects.all()
        serializer = AnnouncementCategorySerializer(categories, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='category_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        operation_summary='Announcements List',
        operation_description='List of Announcements',
        responses={200: AnnouncementSerializer(many=True)},
        tags=['Announcement']
    )
    def announcement_list(self, request):
        param_serializer = ParamValidateSerializer(data=request.query_params, context={'request': request})
        if not param_serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=param_serializer.errors)
        category_id = param_serializer.validated_data.get('category_id')
        data = Announcement.objects.filter(category_id=category_id, is_published=True)
        response = get_paginated_announcement(request_data=data, context={'request': request},
                                              page=param_serializer.validated_data.get('page'),
                                              page_size=param_serializer.validated_data.get('page_size'))
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Announcements detail',
        operation_description='Detail of Announcements',
        responses={200: AnnouncementSerializer()},
        tags=['Announcement']
    )
    def announcement_detail(self, request, pk):
        announcement = Announcement.objects.filter(id=pk, is_published=True).first()
        if not announcement:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='Announcement not found')

        today = timezone.now().date()
        customer = create_customer(request)
        content_viewer = ContentViewer.objects.filter(content_id=pk, customer=customer, content_type=1).first()
        if not content_viewer:
            ContentViewer.objects.create(content_id=pk, customer=customer, content_type=1, view_day=today)
            announcement.views += 1
            announcement.save(update_fields=['views'])
        elif content_viewer.view_day < today:
            ContentViewer.objects.update(content_id=pk, customer=customer, content_type=1, view_day=today)
            announcement.views += 1
            announcement.save(update_fields=['views'])
        serializer = AnnouncementSerializer(announcement, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
