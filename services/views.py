from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import (
    CategoryOrganization, Organization, Service, Training,
    TrainingMedia, TrainingTest, TrainingTestAnswer,
    ElectronLibraryCategory, ElectronLibrary, News, HonestyTest,
    HonestyTestAnswer, CorruptionRating, CorruptionType, Corruption,
    CorruptionMaterial, CitizenOversight, ConflictAlertType,
    ConflictAlert, RelatedPerson, Profession, ProfessionalEthics, OfficerAdvice,
    ReportType, ViolationReport, ViolationReportFile, OrganizationSummary,
    GuiltyPerson, TechnicalSupport
)

from .serializers import (
    CategoryOrganizationSerializer, OrganizationSerializer, ServiceSerializer,
    TrainingSerializer, TrainingMediaSerializer, TrainingTestSerializer,
    TrainingTestAnswerSerializer, ElectronLibraryCategorySerializer,
    ElectronLibrarySerializer, NewsSerializer, HonestyTestSerializer,
    HonestyTestAnswerSerializer, CorruptionRatingSerializer, CorruptionTypeSerializer,
    CorruptionSerializer, CorruptionMaterialSerializer, CitizenOversightSerializer,
    ConflictAlertSerializer, ConflictAlertTypeSerializer, RelatedPersonSerializer,
    ProfessionSerializer, ProfessionalEthicsSerializer, OfficerAdviceSerializer,
    ReportTypeSerializer, ViolationReportSerializer, ViolationReportFileSerializer,
    OrganizationSummarySerializer, GuiltyPersonSerializer, TechnicalSupportSerializer
)
