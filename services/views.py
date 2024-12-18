from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import (
    CategoryOrganization, Organization, Service, Training,
    TrainingTest, TrainingTestAnswer, ElectronLibraryCategory,
    ElectronLibrary, News, HonestyTest, HonestyTestAnswer,
    CorruptionType, Corruption, CitizenOversight, ConflictAlertType,
    ConflictAlert, Profession, ProfessionalEthics,
    OfficerAdvice, ReportType
)

from .serializers import (
    CategoryOrganizationSerializer, OrganizationSerializer, ServiceSerializer,
    TrainingSerializer, TrainingTestSerializer, TrainingTestAnswerSerializer,
    ElectronLibraryCategorySerializer, ElectronLibrarySerializer, NewsSerializer,
    HonestyTestSerializer, HonestyTestAnswerSerializer, CorruptionRatingSerializer,
    CorruptionTypeSerializer, CorruptionSerializer, CitizenOversightSerializer,
    ConflictAlertSerializer, ConflictAlertTypeSerializer, ProfessionSerializer,
    ProfessionalEthicsSerializer, OfficerAdviceSerializer, ReportTypeSerializer,
    ViolationReportSerializer, TechnicalSupportSerializer
)


class OrganizationViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: OrganizationSerializer()},
        tags=['Organization']
    )
    def organization_list(self, request):
        data = Organization.objects.all()
        serializer = OrganizationSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: OrganizationSerializer()},
        tags=['Organization']
    )
    def organization(self, request, pk):
        data = Organization.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = OrganizationSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: CategoryOrganizationSerializer()},
        tags=['Organization']
    )
    def organization_category_list(self, request):
        data = CategoryOrganization.objects.all()
        serializer = CategoryOrganizationSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ServiceSerializer()},
        tags=['Organization']
    )
    def service_list(self, request):
        data = Service.objects.all()
        serializer = ServiceSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ServiceSerializer()},
        tags=['Organization']
    )
    def service(self, request, pk):
        data = Service.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ServiceSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class TrainingViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: TrainingSerializer()},
        tags=['Training']
    )
    def training_list(self, request):
        data = Training.objects.all()
        serializer = TrainingSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: TrainingSerializer()},
        tags=['Training']
    )
    def training(self, request, pk):
        data = Training.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = TrainingSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='training_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Training ID'),
        ],
        responses={200: TrainingTestSerializer()},
        tags=['Training']
    )
    def training_test_list(self, request):
        training_id = request.query_params.get('training_id')
        if not training_id or not training_id.isdigit():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Training ID is required')
        data = TrainingTest.objects.filter(training_id=training_id)
        serializer = TrainingTestSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='training_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Training ID'),
        ],
        responses={200: TrainingTestSerializer()},
        tags=['Training']
    )
    def training_test(self, request, pk):
        training_id = request.query_params.get('training_id')
        if not training_id or not training_id.isdigit():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Training ID is required')
        data = TrainingTest.objects.filter(id=pk, training_id=training_id).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = TrainingTestSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: TrainingTestAnswerSerializer()},
        tags=['Training']
    )
    def training_test_answer(self, request, pk):
        data = TrainingTestAnswer.objects.filter(question_id=pk)
        serializer = TrainingTestAnswerSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ElectronLibraryViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: ElectronLibrarySerializer()},
        tags=['ElectronLibrary']
    )
    def electron_library_list(self, request):
        data = ElectronLibrary.objects.all()
        serializer = ElectronLibrarySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ElectronLibrarySerializer()},
        tags=['ElectronLibrary']
    )
    def electron_library(self, request, pk):
        data = ElectronLibrary.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ElectronLibrarySerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ElectronLibraryCategorySerializer()},
        tags=['ElectronLibrary']
    )
    def electron_library_category(self, request):
        data = ElectronLibraryCategory.objects.all()
        serializer = ElectronLibraryCategorySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class NewsViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: NewsSerializer()},
        tags=['News']
    )
    def news_list(self, request):
        data = News.objects.all()
        serializer = NewsSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: NewsSerializer()},
        tags=['News']
    )
    def news(self, request, pk):
        data = News.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = NewsSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class HonestyViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: HonestyTestSerializer()},
        tags=['HonestyTest']
    )
    def honesty_test_list(self, request):
        data = HonestyTest.objects.all()
        serializer = HonestyTestSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: HonestyTestSerializer()},
        tags=['HonestyTest']
    )
    def honesty_test(self, request, pk):
        data = HonestyTest.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = HonestyTestSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: HonestyTestAnswerSerializer()},
        tags=['HonestyTest']
    )
    def honesty_test_answer(self, request, pk):
        data = HonestyTestAnswer.objects.filter(question_id=pk)
        serializer = HonestyTestAnswerSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class CorruptionRiskRatingViewSet(ViewSet):
    @swagger_auto_schema(
        responses={201: CorruptionRatingSerializer()},
        tags=['CorruptionRating']
    )
    def create_rating(self, request):
        serializer = CorruptionRatingSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)


class CorruptionViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: CorruptionSerializer()},
        tags=['Corruption']
    )
    def corruption_list(self, request):
        data = Corruption.objects.all()
        serializer = CorruptionSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: CorruptionSerializer()},
        tags=['Corruption']
    )
    def corruption(self, request, pk):
        data = Corruption.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = CorruptionSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: CorruptionTypeSerializer()},
        tags=['Corruption']
    )
    def corruption_types(self, request):
        data = CorruptionType.objects.all()
        serializer = CorruptionTypeSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class CitizenOversightViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: CitizenOversightSerializer()},
        tags=['CitizenOversight']
    )
    def citizen_oversight_list(self, request):
        data = CitizenOversight.objects.all()
        serializer = CitizenOversightSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: CitizenOversightSerializer()},
        tags=['CitizenOversight']
    )
    def citizen_oversight(self, request, pk):
        data = CitizenOversight.objects.filter(id=pk).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = CitizenOversightSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ConflictAlertviewSet(ViewSet):
    @swagger_auto_schema(
        request_body=ConflictAlertSerializer(),
        responses={200: ConflictAlertSerializer()},
        tags=['ConflictAlert']
    )
    def create_conflict_alert(self, request):
        serializer = ConflictAlertSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: ConflictAlertTypeSerializer()},
        tags=['ConflictAlert']
    )
    def conflict_alert_types(self, request):
        data = ConflictAlertType.objects.all()
        serializer = ConflictAlertTypeSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
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
        responses={200: ProfessionalEthicsSerializer()},
        tags=['ProfessionalEthics']
    )
    def professional_ethics_list(self, request):
        data = ProfessionalEthics.objects.all()
        serializer = ProfessionalEthicsSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
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
        responses={200: ProfessionSerializer()},
        tags=['ProfessionalEthics']
    )
    def profession_list(self, request):
        data = Profession.objects.all()
        serializer = ProfessionSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class OfficerAdviceViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=OfficerAdviceSerializer(),
        responses={201: OfficerAdviceSerializer()},
        tags=['OfficerAdvice']
    )
    def create_officer_advice(self, request):
        serializer = OfficerAdviceSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: OfficerAdviceSerializer()},
        tags=['OfficerAdvice']
    )
    def officer_advice_list(self, request):
        data = OfficerAdvice.objects.all()
        serializer = OfficerAdviceSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ViolationReportViewSet(ViewSet):
    @swagger_auto_schema(
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
        responses={200: ReportTypeSerializer()},
        tags=['ViolationReport']
    )
    def report_types(self, request):
        data = ReportType.objects.all()
        serializer = ReportTypeSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class TechnicalSupportViewSet(ViewSet):
    @swagger_auto_schema(
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
