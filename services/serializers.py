from rest_framework import serializers
from .models import (
    CategoryOrganization, Organization, Service, Training,
    TrainingMedia, TrainingTest, TrainingTestAnswer,
    ElectronLibraryCategory, ElectronLibrary, News, HonestyTest,
    HonestyTestAnswer, CorruptionRating, CorruptionType, Corruption,
    CorruptionMaterial, CitizenOversight,
    ConflictAlert, Profession, ProfessionalEthics,
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
        fields = ('id', 'name', 'author', 'edition_author', 'edition_type', 'edition_year', 'description',
                  'file', 'category')


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


class ConflictAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictAlert
        fields = ('id', 'organization_name', 'organization_director_full_name', 'organization_director_position',
                  'description', 'additional_description', 'type', 'employee_full_name', 'employee_position',
                  'employee_passport_number', 'employee_passport_series', 'employee_passport_taken_date',
                  'employee_legal_entity_name', 'employee_legal_entity_data', 'employee_stir_number',
                  'related_persons_full_name', 'related_persons_passport_number', 'related_persons_passport_series',
                  'related_persons_passport_taken_date', 'related_persons_legal_entity_name',
                  'related_persons_stir_number', 'related_persons_kinship_data')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'name', 'description')


class ProfessionalEthicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalEthics
        fields = ('id', 'title', 'description', 'profession')


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
