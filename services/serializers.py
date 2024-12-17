from rest_framework import serializers
from .models import (
    CategoryOrganization, Organization, Service, Training,
    TrainingMedia, TrainingTest, TrainingTestAnswer,
    ElectronLibraryCategory, ElectronLibrary, News, HonestyTest,
    HonestyTestAnswer, CorruptionRating, CorruptionType, Corruption,
    CorruptionMaterial, CitizenOversight, ConflictAlertType,
    ConflictAlert, RelatedPerson, Profession, ProfessionalEthics,
    OfficerAdvice, ReportType, ViolationReport, ViolationReportFile,
    GuiltyPerson, TechnicalSupport
)


class CategoryOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryOrganization
        fields = ('id', 'name')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'category', 'name', 'phone_number', 'email', 'region', 'district', 'address', 'link')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'organization')


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ('id', 'author', 'name', 'image', 'description', 'number_participants')


class TrainingMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingMedia
        fields = ('id', 'training', 'file', 'order', 'type')


class TrainingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTest
        fields = ('id', 'training', 'question')


class TrainingTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTestAnswer
        fields = ('id', 'question', 'answer', 'is_true')


class ElectronLibraryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronLibraryCategory
        fields = ('id', 'name')


class ElectronLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronLibrary
        fields = ('id', 'title', 'file', 'category')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'short_description', 'description', 'image', 'is_published', 'is_published_date')


class HonestyTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTest
        fields = ('id', 'question')


class HonestyTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestAnswer
        fields = ('id', 'question', 'answer')


class CorruptionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorruptionRating
        fields = ('id', 'corruption', 'rating')


class CorruptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorruptionType
        fields = ('id', 'name')


class CorruptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corruption
        fields = ('id', 'title', 'description', 'type')


class CorruptionMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorruptionMaterial
        fields = ('id', 'corruption', 'file')


class CitizenOversightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenOversight
        fields = ('id', 'control_method', 'control_result', 'description')


class ConflictAlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictAlertType
        fields = ('id', 'name')


class ConflictAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictAlert
        fields = ('id', 'organization_name', 'description', 'event_date', 'action_taken', 'type')


class RelatedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedPerson
        fields = ('id', 'conflict_alert', 'first_name', 'last_name', 'position', 'informant_jshshr', 'informant')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'name', 'description')


class ProfessionalEthicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalEthics
        fields = ('id', 'title', 'description', 'moral_dilemma', 'link', 'profession')


class OfficerAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerAdvice
        fields = ('id', 'officer', 'professional_ethics', 'comment')


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ('id', 'name')


class ViolationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationReport
        fields = ('id', 'organization', 'event_time', 'region', 'district', 'status', 'report_type', 'comment')


class ViolationReportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationReportFile
        fields = ('id', 'report', 'file', 'comment')


class GuiltyPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiltyPerson
        fields = ('id', 'report', 'full_name', 'position', 'contact')


class TechnicalSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSupport
        fields = ('id', 'image', 'comment')
