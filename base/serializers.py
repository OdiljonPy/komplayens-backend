from .models import Region, District, FAQ, AboutUs, CorruptionRisk, CorruptionCase
from rest_framework import serializers

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
