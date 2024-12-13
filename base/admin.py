from django.contrib import admin
from .models import Region, District, FAQ, AboutUs, CorruptionRisk, CorruptionCase


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'type')
    list_display_links = ('id', 'question')


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'type')
    list_display_links = ('id', 'link')


@admin.register(CorruptionRisk)
class CorruptionRiskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_desc')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(CorruptionCase)
class CorruptionCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'corruption')
