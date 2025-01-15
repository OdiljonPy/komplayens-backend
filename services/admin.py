from django.contrib import admin
from .models import (
    CategoryOrganization, Organization, Training,
    TrainingMedia, ElectronLibraryCategory, ElectronLibrary, News,
    HonestyTest, HonestyTestAnswer, ConflictAlert,
    Profession, ProfessionalEthics, OfficerAdvice, ReportType,
    ViolationReport, TechnicalSupport, TrainingCategory,
    NewsCategory, HonestyTestCategory, HonestyTestStatistic,
    ViolationFile, GuiltyPerson, HonestyTestResult,
    CorruptionRisk,  AnnouncementCategory, Announcement
)


@admin.register(CategoryOrganization)
class CategoryOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'address')
    list_display_links = ('id', 'name', 'phone_number')
    search_fields = ('name', 'phone_number', 'address', 'district__name', 'region__name', 'email')
    list_filter = ('region', 'district')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(TrainingMedia)
class TrainingMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'type')
    list_display_links = ('id', 'order')
    search_fields = ('order',)
    list_filter = ('type',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description',)
    list_filter = ('is_published',)


@admin.register(ElectronLibraryCategory)
class ElectronLibraryCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(ElectronLibrary)
class ElectronLibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'category', 'is_published')
    list_display_links = ('id', 'name', 'author')
    search_fields = ('name', 'author', 'category__name')
    list_filter = ('is_published', 'category')


@admin.register(HonestyTest)
class HonestyTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    list_display_links = ('id', 'question')
    search_fields = ('question',)


@admin.register(HonestyTestCategory)
class HonestyTestCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(HonestyTestAnswer)
class HonestyTestAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    list_display_links = ('id', 'question')
    search_fields = ('question__question', 'answer')


@admin.register(HonestyTestStatistic)
class HonestyTestStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_type', 'organization', 'customer')
    list_display_links = ('id', 'test_type')


@admin.register(HonestyTestResult)
class HonestyTestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'test')
    list_display_links = ('id', 'customer')


@admin.register(ConflictAlert)
class ConflictAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name', 'organization_director_full_name', 'type')
    list_display_links = ('id', 'organization_name')
    search_fields = ('organization_name',)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


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
    list_display = ('id', 'organization', 'event_time', 'report_type')
    list_display_links = ('id', 'organization')
    list_filter = ('report_type',)
    search_fields = ('comment',)


@admin.register(TechnicalSupport)
class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
    list_display_links = ('id', 'comment')
    search_fields = ('comment',)


@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'report')
    list_display_links = ('id', 'report')


@admin.register(GuiltyPerson)
class GuiltyPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'report')
    list_display_links = ('id', 'full_name',)


@admin.register(CorruptionRisk)
class CorruptionRiskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ('id', 'name')
@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

