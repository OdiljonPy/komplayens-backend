from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.conf import settings
from .models import (
    HonestyTest, HonestyTestAnswer, GuiltyPerson,
    ViolationFile, ConflictAlert, OfficerAdvice,
    ViolationReport, TechnicalSupport, HonestyTestResult,
    News, HonestyTestStatistic
)


class ParamValidateSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    category_id = serializers.IntegerField(required=False)
    q = serializers.CharField(required=False, default='')
    popular = serializers.BooleanField(allow_null=True, required=False)
    order_by = serializers.ChoiceField(choices=('new', 'old'), required=False, default='new')

    def validate(self, data):
        if data.get('page_size') < 1 or data.get('page') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                     message='page and page_size must be positive integer')
        if data.get('category_id') is not None and data.get('category_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Category id must be positive integer')
        return data


class HonestyParamSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    organization_id = serializers.IntegerField(required=False)

    def validate(self, data):
        if data.get('category_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Category id must be positive integer')
        if data.get('organization_id') is not None and data.get('organization_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Organization id must be positive integer')
        return data


class CategoryOrganizationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class OrganizationSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['address'] = serializers.CharField(source=f'address_{language}')

    id = serializers.IntegerField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
    phone_number2 = serializers.CharField(max_length=15)
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


class TrainingCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class TrainingSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    image = serializers.ImageField()
    description = serializers.CharField()
    video = serializers.URLField()
    video_length = serializers.FloatField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    views = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class TrainingMediaSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['filename'] = serializers.CharField(source=f'filename_{language}')
        self.fields['video_title'] = serializers.CharField(source=f'video_title_{language}')

    id = serializers.IntegerField(read_only=True)
    training = serializers.PrimaryKeyRelatedField(read_only=True)
    filename = serializers.CharField()
    file = serializers.FileField()
    video = serializers.URLField()
    video_title = serializers.CharField()
    order = serializers.IntegerField()
    type = serializers.CharField()


class TrainingDetailSerializer(TrainingSerializer):
    materials = TrainingMediaSerializer(many=True, source='training_materials')


class ElectronLibraryCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=40)


class ElectronLibrarySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['author'] = serializers.CharField(source=f'author_{language}')
        self.fields['edition_author'] = serializers.CharField(source=f'edition_author_{language}')
        self.fields['edition_type'] = serializers.CharField(source=f'edition_type_{language}')
        self.fields['short_description'] = serializers.CharField(source=f'short_description_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=80)
    short_description = serializers.CharField(max_length=400)
    author = serializers.CharField(max_length=100)
    edition_author = serializers.CharField(max_length=100)
    edition_type = serializers.CharField(max_length=100)
    edition_year = serializers.DateField()
    file = serializers.FileField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)


class NewsCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class NewsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['short_description'] = serializers.CharField(source=f'short_description_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    published_date = serializers.DateField()
    views = serializers.IntegerField()


class NewsDetailSerializer(NewsSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = getattr(instance.category, 'id')
        additional = News.objects.filter(
            is_published=True, category_id=category).exclude(id=instance.id).order_by('-views')[:3]
        if not additional:
            additional = News.objects.filter(is_published=True).exclude(id=instance.id).order_by('-views')[:3]
        data['additional'] = NewsSerializer(additional, many=True, context=self.context).data
        return data


class HonestyTestCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    image = serializers.ImageField()


class HonestyTestAnswerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['answer'] = serializers.CharField(source=f'answer_{language}')

    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField()
    is_true = serializers.BooleanField()


class HonestyTestDefaultAnswerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['answer'] = serializers.CharField(source=f'answer_{language}')

    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField()
    is_true = serializers.SerializerMethodField()

    def get_is_true(self, obj):
        return


class HonestyTestUserResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestResult
        fields = ('answer', 'result')


class HonestyTestDefaultSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['question'] = serializers.CharField(source=f'question_{language}')
        self.fields['advice'] = serializers.CharField(source=f'advice_{language}')

    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    advice = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = serializers.SerializerMethodField()
    user_result = serializers.SerializerMethodField()

    def get_advice(self, obj):
        return

    def get_user_result(self, obj):
        return {}

    def get_answers(self, obj):
        return HonestyTestDefaultAnswerSerializer(obj.test_honest,
            many=True, read_only=True, context=self.context).data


class HonestyTestSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['question'] = serializers.CharField(source=f'question_{language}')
        self.fields['advice'] = serializers.CharField(source=f'advice_{language}')

    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    advice = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = serializers.SerializerMethodField()
    user_result = serializers.SerializerMethodField()

    def get_user_result(self, obj):
        customer = self.context.get('customer')
        result = obj.test_result.filter(customer=customer).first()
        if result:
            return HonestyTestUserResultSerializer(result).data
        return None

    def get_answers(self, obj):
        return HonestyTestAnswerSerializer(obj.test_honest, many=True,
                                           read_only=True, context=self.context).data


class HonestyTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestResult
        fields = ('id', 'test', 'answer', 'result')
        extra_kwargs = {'result': {'required': False}}

    def validate(self, data):
        test = data.get('test')
        answer = data.get('answer')
        test_id = getattr(test, 'id', None)
        answer_id = getattr(answer, 'id', None)

        if not HonestyTest.objects.filter(id=test_id):
            raise CustomApiException(ErrorCodes.NOT_FOUND, message=f"Test ID {test_id} not found.")

        if answer_id and not HonestyTestAnswer.objects.filter(id=answer_id, question_id=test_id):
            raise CustomApiException(ErrorCodes.NOT_FOUND,
                                     message=f"Test ID {test_id} and answer ID {answer_id} doesn't match.")

        return data

    def create(self, validated_data):
        from authentication.utils import create_customer
        customer = create_customer(self.context.get('request'))
        answer = validated_data.get('answer')
        result = getattr(answer, 'is_true', False)
        return HonestyTestResult.objects.create(
            test=validated_data.get('test'),
            answer=validated_data.get('answer'),
            result=result,
            customer=customer
        )


class HonestyTestSendResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    answer = serializers.PrimaryKeyRelatedField(read_only=True)
    result = serializers.BooleanField()
    honesty_test = HonestyTestSerializer(read_only=True, source='test')


class HonestyTestResultRequestSerializer(serializers.Serializer):
    test = serializers.IntegerField()
    answer = serializers.IntegerField()

    def validate(self, data):
        if data.get('question') is not None and data.get('question') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Question id must be positive integer')
        if data.get('answer') is not None and data.get('answer') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Answer id must be positive integer')


class HonestyTestResultStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonestyTestStatistic
        fields = ('id', 'test_type', 'customer', 'organization')


class CorruptionRiskSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['short_desc'] = serializers.CharField(source=f'short_desc_{language}')
        self.fields['result'] = serializers.CharField(source=f'result_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    short_desc = serializers.CharField()
    image = serializers.ImageField()
    form_url = serializers.URLField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    result = serializers.CharField()
    status = serializers.IntegerField()


class CorruptionRiskMediaSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['filename'] = serializers.CharField(source=f'filename_{language}')

    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField()
    file = serializers.FileField()


class ConflictAlertTypeSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('type') is not None and data.get('type') not in [1, 2, 3]:
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class ProfessionalEthicsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')
        self.fields['case'] = serializers.CharField(source=f'case_{language}')

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    case = serializers.CharField()
    profession = serializers.PrimaryKeyRelatedField(read_only=True)


class OfficerAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerAdvice
        fields = ('id', 'officer', 'professional_ethics', 'comment')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at'] = instance.created_at
        data['officer_full_name'] = getattr(
            instance.officer, 'first_name', '') + ' ' + getattr(instance.officer, 'last_name', '')
        return data


class ReportTypeSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

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


class PaginatorValidator(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs.get('page', 0) < 1 or attrs.get('page_size', 0) < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='page and page_size must be greater than 1')
        if (attrs.get('from_date') and attrs.get('to_date')) and (attrs.get('from_date') > attrs.get('to_date')):
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='From date cannot be greater than To date')
        return super().validate(attrs)


class TrainingParamValidator(PaginatorValidator):
    category_id = serializers.IntegerField(required=False)
    q = serializers.CharField(required=False, default='')
    order_by = serializers.ChoiceField(choices=('new', 'old'), required=False, default='new')
    popular = serializers.BooleanField(allow_null=True, default=False)

    def validate(self, attrs):
        if attrs.get('category_id') is not None and attrs.get('category_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='category_id must be greater than 1')
        return super().validate(attrs)


class NewsParamValidator(PaginatorValidator):
    category_id = serializers.IntegerField(required=False)
    popular = serializers.BooleanField(allow_null=True, default=False)
    order_by = serializers.ChoiceField(choices=('old', 'new'), required=False, default='new')

    def validate(self, attrs):
        if attrs.get('category_id') is not None and attrs.get('category_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='category_id must be greater than 1')
        return super().validate(attrs)


class ProfessionalEthicsParamValidator(PaginatorValidator):
    q = serializers.CharField(required=False, default='')
    profession_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if attrs.get('profession_id') is not None and attrs.get('profession_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='profession_id must be greater than 1')
        return super().validate(attrs)


class OfficerAdviceParamValidator(PaginatorValidator):
    professional_ethics = serializers.IntegerField(required=True)

    def validate(self, attrs):
        if attrs.get('professional_ethics', 0) < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='professional_ethics must be greater than 1')
        return super().validate(attrs)


class ViolationReportCreateSerializer(serializers.Serializer):
    organization = serializers.IntegerField(required=True)
    event_time = serializers.DateTimeField(required=True)
    region = serializers.IntegerField(required=True)
    district = serializers.IntegerField(required=True)
    report_type = serializers.IntegerField(required=True)
    comment = serializers.CharField(required=True)
    informant_full_name = serializers.CharField(required=False)
    informant_phone_number = serializers.CharField(required=False)
    informant_email = serializers.EmailField(required=False)
    is_anonim = serializers.BooleanField(required=False, default=False)
    file = serializers.FileField(required=False)
    full_name = serializers.CharField(required=True)
    position = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False)


class CorruptionRiskParamValidator(PaginatorValidator):
    order_by = serializers.ChoiceField(choices=('new', 'old'), required=False, default='new')
    status = serializers.IntegerField(required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs.get('status') and attrs.get('status', 0) < 1 or attrs.get('status', 0) > 2:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='status must be between 1 and 2')
        return super().validate(attrs)


class AnnouncementCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class AnnouncementSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    id = serializers.IntegerField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField()
    views = serializers.PrimaryKeyRelatedField(read_only=True)
    published_date = serializers.DateField()

    def get_category(self, obj):
        return obj.category.name


class HandoutCategorySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class HandoutSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    file = serializers.FileField()
    type = serializers.CharField()
