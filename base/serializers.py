from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from config import settings

class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    region = serializers.PrimaryKeyRelatedField(read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['region_name'] = serializers.CharField(source=f'region.name_{language}')


class FAQSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField()
    type = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['question'] = serializers.CharField(source=f'question_{language}')
        self.fields['answer'] = serializers.CharField(source=f'answer_{language}')


class AboutUsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    short_description = serializers.CharField()
    image = serializers.ImageField()
    type = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['short_description'] = serializers.CharField(source=f'short_description_{language}')


class TypeSerializer(serializers.Serializer):
    type = serializers.IntegerField()

    def validate(self, data):
        if data.get('type') not in [1, 2, 3]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='FAQ type must be 1, 2, or 3')
        return data


class AboutUsTypeSerializer(TypeSerializer):
    def validate(self, data):
        if data.get('type') not in [1, 2, 3]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='AboutUs type must be 1, 2 or 3')
        return data


class BannerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    short_description = serializers.CharField()
    image = serializers.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['short_description'] = serializers.CharField(source=f'short_description_{language}')


class StatisticYearSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField()


class RainbowStatisticSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year_id = serializers.IntegerField()
    high = serializers.FloatField()
    satisfactory = serializers.FloatField()
    unsatisfactory = serializers.FloatField()


class LinerStatisticSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year_id = serializers.IntegerField()
    name = serializers.CharField()
    percentage = serializers.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')


class StatisticParamSerializer(serializers.Serializer):
    year_id = serializers.IntegerField(required=False)

    def validate(self, data):
        if data.get('year_id') and data.get('year_id') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Statistic year_id must be positive integer')
        return data
