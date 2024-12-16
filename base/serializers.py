from .models import Region, District, FAQ, AboutUs, CorruptionRisk, CorruptionCase
from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    class Meta:
        model = District
        fields = ['id', 'name', 'region', 'region_name']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'type']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'short_desc', 'link', 'type']


class CorruptionRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorruptionRisk
        fields = ['id', 'name', 'short_desc', 'more_desc', 'useful_advice', 'legal_document']


class CorruptionCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorruptionCase
        fields = ['id', 'corruption', 'description']


class TypeSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=False, default=1)

    def validate(self, data):
        if data.get('type') and data.get('type') not in [1, 2, 3]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='FAQ type must be 1, 2, or 3')
        return data


class AboutUsTypeSerializer(TypeSerializer):
    def validate(self, data):
        if data.get('type') and data.get('type') not in [1, 2, 3, 4]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='AboutUs type must be 1, 2, 3 or 4')
        return data
