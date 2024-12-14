from django.contrib import admin
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


@admin.register(CategoryOrganization)
class CategoryOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'address')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone_number', 'address', 'district__name', 'region__name', 'email')
    list_filter = ('region', 'district')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'organization__name')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number_participants')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(TrainingMedia)
class TrainingMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'type')
    list_display_links = ('id', 'order')
    search_fields = ('order',)
    list_filter = ('type',)


@admin.register(TrainingTest)
class TrainingTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'training', 'question')
    list_display_links = ('id', 'training')
    search_fields = ('training__name', 'question')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'is_published_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description', 'short_description', 'is_published_date')
    list_filter = ('is_published',)
