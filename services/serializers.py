from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import (HonestyTest, HonestyTestAnswer, GuiltyPerson,
                     ViolationFile, ConflictAlert, OfficerAdvice,
                     ViolationReport, TechnicalSupport, HonestyTestResult
)


class CategoryOrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class OrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
    phone_number_2 = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    region = serializers.PrimaryKeyRelatedField(read_only=True)
    district = serializers.PrimaryKeyRelatedField(read_only=True)
    address = serializers.CharField()
    weblink = serializers.URLField()
    instagram = serializers.URLField()
    telegram = serializers.URLField()
    facebook = serializers.URLField()
    twitter = serializers.URLField()
    youtube = serializers.URLField()


class ServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    organization = serializers.PrimaryKeyRelatedField(read_only=True)


class  TrainingCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class TrainingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    image = serializers.ImageField()
    description = serializers.CharField()
    video = serializers.URLField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    is_published = serializers.BooleanField()


class TrainingMediaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    training = serializers.PrimaryKeyRelatedField(read_only=True)
    filename = serializers.CharField()
    file = serializers.FileField()
    video = serializers.URLField()
    video_title = serializers.CharField()
    order = serializers.IntegerField()
    type = serializers.CharField()


class ElectronLibraryCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=40)


class ElectronLibrarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=80)
    author =serializers.CharField(max_length=100)
    edition_author = serializers.CharField(max_length=100)
    edition_type = serializers.CharField(max_length=100)
    edition_year = serializers.DateField()
    file = serializers.FileField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    is_published = serializers.BooleanField()


class NewsCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    is_published = serializers.BooleanField()
    published_date = serializers.DateField()
    view_count = serializers.IntegerField()


class HonestyTestCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    image = serializers.ImageField()


class HonestyTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTest
        fields = ('id', 'question', 'advice', 'category')


class HonestyTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestAnswer
        fields = ('id', 'question', 'answer', 'image', 'is_true')


class HonestyTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestResult
        fields = ('id', 'customer', 'test', 'answer', 'result')


class CorruptionRiskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    short_desc = serializers.CharField()
    image = serializers.ImageField()
    form_url = serializers.URLField()
    excel_url = serializers.URLField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    result = serializers.CharField()
    status = serializers.IntegerField()


class ConflictAlertTypeSerializer(serializers.Serializer):
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


class ProfessionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class ProfessionalEthicsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    case = serializers.CharField()
    profession = serializers.PrimaryKeyRelatedField(read_only=True)


class OfficerAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerAdvice
        fields = ('id', 'officer', 'professional_ethics', 'comment')


class ReportTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class ViolationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationReport
        fields = ('id', 'organization', 'event_time', 'region', 'district', 'report_type', 'comment',
                  'informant_full_name', 'informant_phone_number', 'informant_email', 'is_anonim')


class GuiltyPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiltyPerson
        fields = ('id', 'report', 'full_name', 'position', 'phone_number')


class ViolationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationFile
        fields = ('id', 'report', 'file')


class TechnicalSupportSerializer(serializers.Serializer):
    class Meta:
        model = TechnicalSupport
        fields = ('id', 'image', 'comment')
