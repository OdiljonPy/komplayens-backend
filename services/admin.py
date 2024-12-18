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


@admin.register(TrainingTestAnswer)
class TrainingTestAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'is_true')
    list_display_links = ('id', 'question')
    search_fields = ('id', 'question__question', 'answer')


@admin.register(ElectronLibraryCategory)
class ElectronLibraryCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(ElectronLibrary)
class ElectronLibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'category__name')


@admin.register(HonestyTest)
class HonestyTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    list_display_links = ('id', 'question')
    search_fields = ('question',)


@admin.register(HonestyTestAnswer)
class HonestyTestAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    list_display_links = ('id', 'question')
    search_fields = ('question__question', 'answer')


@admin.register(CorruptionRating)
class CorruptionRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'corruption', 'rating')
    list_display_links = ('id', 'corruption',)


@admin.register(CorruptionType)
class CorruptionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Corruption)
class CorruptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('type',)


@admin.register(CorruptionMaterial)
class CorruptionMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'corruption')
    list_display_links = ('id', 'corruption',)


@admin.register(CitizenOversight)
class CitizenOversightAdmin(admin.ModelAdmin):
    list_display = ('id', 'control_method', 'control_result')
    list_display_links = ('id', 'control_method', 'control_result')
    search_fields = ('control_method', 'control_result')


@admin.register(ConflictAlertType)
class ConflictAlertTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(ConflictAlert)
class ConflictAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name', 'event_date', 'action_taken')
    list_display_links = ('id', 'organization_name')
    search_fields = ('organization_name', 'action_taken')


@admin.register(RelatedPerson)
class RelatedPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'conflict_alert')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(ProfessionalEthics)
class ProfessionalEthicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'profession')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('profession',)


@admin.register(OfficerAdvice)
class OfficerAdviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'officer', 'professional_ethics')
    list_display_links = ('id', 'officer')


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(ViolationReport)
class ViolationReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'event_time', 'status', 'report_type')
    list_display_links = ('id', 'organization')
    list_filter = ('report_type', 'status')
    search_fields = ('comment',)


@admin.register(ViolationReportFile)
class ViolationReportFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'report')
    list_display_links = ('id', 'report')
    search_fields = ('comment',)


@admin.register(GuiltyPerson)
class GuiltyPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position')
    list_display_links = ('id', 'full_name')
    search_fields = ('full_name', 'position')


@admin.register(TechnicalSupport)
class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
    list_display_links = ('id', 'comment')
    search_fields = ('comment',)

