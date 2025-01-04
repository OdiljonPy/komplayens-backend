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
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


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


class TypeSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('type') and data.get('type') not in [1, 2, 3]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Type must be 1, 2, or 3')
        return data


class ConflictAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictAlert
        fields = ('id', 'organization_name', 'organization_director_full_name', 'organization_director_position',
                  'description', 'additional_description', 'type', 'employee_full_name', 'employee_position',
                  'employee_passport_number', 'employee_passport_series', 'employee_passport_taken_date',
                  'employee_legal_entity_name', 'employee_legal_entity_data', 'employee_stir_number',
                  'related_persons_full_name', 'related_persons_passport_number', 'related_persons_passport_series',
                  'related_persons_passport_taken_date', 'related_persons_legal_entity_name',
                  'related_persons_stir_number', 'related_persons_kinship_data', 'filled_date')

    def validate(self, attrs):
        if attrs.get('employee_passport_number') and len(attrs.get('employee_passport_number')) != 14:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                    message='The employee passport number should be 14 characters long')
        if attrs.get('related_persons_passport_number') and len(attrs.get('related_persons_passport_number')) != 14:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                    message='The related persons passport number should be 14 characters long')
        if attrs.get('employee_passport_series') and len(attrs.get('employee_passport_series')) != 9:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                    message='The employee passport series should be 9 characters long')
        if attrs.get('related_persons_passport_series') and len(attrs.get('related_persons_passport_series')) != 9:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                    message='The related persons series should be 9 characters long')
        return attrs

#
# class ConflictAlertFileOneSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     organization_name = serializers.CharField()
#     organization_director_full_name = serializers.CharField()
#     organization_director_position = serializers.CharField()
#     employee_full_name = serializers.CharField()
#     employee_position = serializers.CharField()
#     employee_passport_number = serializers.CharField()
#     employee_passport_series = serializers.CharField()
#     employee_passport_taken_date = serializers.CharField()
#     employee_legal_entity_name = serializers.CharField()
#     employee_stir_number = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_passport_series = serializers.CharField()
#     related_persons_passport_taken_date = serializers.CharField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     description=serializers.CharField()
#
#
# class ConflictAlertFileOneSerializerRequest(serializers.Serializer):
#     organization_name = serializers.CharField()
#     organization_director_full_name = serializers.CharField()
#     organization_director_position = serializers.CharField()
#     employee_full_name = serializers.CharField()
#     employee_position = serializers.CharField()
#     employee_passport_number = serializers.CharField()
#     employee_passport_series = serializers.CharField()
#     employee_passport_taken_date = serializers.DateField()
#     employee_legal_entity_name = serializers.CharField()
#     employee_stir_number = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_passport_series = serializers.CharField()
#     related_persons_passport_taken_date = serializers.DateField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     description=serializers.CharField()
#     type=serializers.IntegerField()
#
#     def validate(self, attrs):
#         if attrs.get('employee_passport_number') and len(attrs.get('employee_passport_number')) != 14:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The employee passport number should be 14 characters long')
#         if attrs.get('related_persons_passport_number') and len(attrs.get('related_persons_passport_number')) != 14:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The related persons passport number should be 14 characters long')
#         if attrs.get('employee_passport_series') and len(attrs.get('employee_passport_series')) != 9:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The employee passport series should be 9 characters long')
#         if attrs.get('related_persons_passport_series') and len(attrs.get('related_persons_passport_series')) != 9:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The related persons series should be 9 characters long')
#         if attrs.get('type') and attrs.get('type') != 1:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='The type should be 1')
#         return attrs
#
#     def create(self, validated_data):
#         return ConflictAlert.objects.create(**validated_data)
#
#
# class ConflictAlertFileTwoSerializerRequest(serializers.Serializer):
#     employee_full_name = serializers.CharField()
#     employee_position = serializers.CharField()
#     employee_passport_number = serializers.CharField()
#     employee_passport_series = serializers.CharField()
#     employee_passport_taken_date = serializers.CharField()
#     employee_legal_entity_name = serializers.CharField()
#     employee_stir_number = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_passport_series = serializers.CharField()
#     related_persons_passport_taken_date = serializers.CharField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     description = serializers.CharField()
#     additional_description = serializers.CharField()
#     type = serializers.IntegerField()
#
#
#     def validate(self, attrs):
#         if attrs.get('related_persons_passport_number') and len(attrs.get('related_persons_passport_number')) != 14:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The related persons passport number should be 14 characters long')
#         if attrs.get('related_persons_passport_series') and len(attrs.get('related_persons_passport_series')) != 9:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The related persons series should be 9 characters long')
#         if attrs.get('employee_passport_number') and len(attrs.get('employee_passport_number')) != 14:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The employee passport number should be 14 characters long')
#         if attrs.get('employee_passport_series') and len(attrs.get('employee_passport_series')) != 9:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
#                                      message='The employee passport series should be 9 characters long')
#         if attrs.get('type') and attrs.get('type') != 2:
#             raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='The type should be 2')
#         return attrs
#
#     def create(self, validated_data):
#         return ConflictAlert.objects.create(**validated_data)
#
#
# class ConflictAlertFileTwoSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     employee_full_name = serializers.CharField()
#     employee_position = serializers.CharField()
#     employee_passport_number = serializers.CharField()
#     employee_passport_series = serializers.CharField()
#     employee_passport_taken_date = serializers.CharField()
#     employee_legal_entity_name = serializers.CharField()
#     employee_stir_number = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_passport_series = serializers.CharField()
#     related_persons_passport_taken_date = serializers.CharField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     description = serializers.CharField()
#     additional_description = serializers.CharField()
#
#
# class ConflictAlertFileThreeSerializerRequest(serializers.Serializer):
#     employee_full_name = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     related_persons_kinship_data = serializers.CharField()
#     employee_legal_entity_data = serializers.CharField()
#     type = serializers.IntegerField()
#
#     def validate(self, attrs):
#         if attrs.get('related_persons_passport_number') and len(attrs.get('related_persons_passport_number')) != 14:
#             raise serializers.ValidationError('The related persons passport number should be 14 characters long')
#         if attrs.get('type') and attrs.get('type') != 3:
#             raise serializers.ValidationError('The type should be 3')
#         return attrs
#
#     def create(self, validated_data):
#         return ConflictAlert.objects.create(**validated_data)
#
#
# class ConflictAlertFileThreeSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     employee_full_name = serializers.CharField()
#     related_persons_full_name = serializers.CharField()
#     related_persons_passport_number = serializers.CharField()
#     related_persons_legal_entity_name = serializers.CharField()
#     related_persons_stir_number = serializers.CharField()
#     related_persons_kinship_data = serializers.CharField()
#     employee_legal_entity_data = serializers.CharField()


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
