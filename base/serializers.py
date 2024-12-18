from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    region = serializers.PrimaryKeyRelatedField(read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)


class FAQSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField()
    type = serializers.IntegerField()


class AboutUsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    short_desc = serializers.CharField()
    link = serializers.CharField()
    type = serializers.IntegerField()


class CorruptionRiskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    short_desc = serializers.CharField()
    more_desc = serializers.CharField()
    useful_advice = serializers.CharField()
    legal_document = serializers.FileField()


class CorruptionCaseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    corruption = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField()


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
