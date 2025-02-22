from modeltranslation.translator import translator, TranslationOptions
from .models import (
    CategoryOrganization, Organization, TrainingCategory, Training,
    TrainingMedia, ElectronLibraryCategory, ElectronLibrary, NewsCategory,
    News, HonestyTestCategory, HonestyTest, HonestyTestAnswer, CorruptionRisk, CorruptionRiskMedia,
    Profession, ProfessionalEthics, ReportType, AnnouncementCategory, Announcement,
    HandoutCategory, Handout
)


class CategoryOrganizationTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(CategoryOrganization, CategoryOrganizationTranslationOptions)


class OrganizationTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Organization, OrganizationTranslationOptions)


class TrainingCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(TrainingCategory, TrainingCategoryTranslationOptions)


class TrainingTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Training, TrainingTranslationOptions)


class TrainingMediaTranslationOptions(TranslationOptions):
    fields = ('filename', 'video_title',)


translator.register(TrainingMedia, TrainingMediaTranslationOptions)


class ElectronLibraryCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ElectronLibraryCategory, ElectronLibraryCategoryTranslationOptions)


class ElectronLibraryTranslationOptions(TranslationOptions):
    fields = ('name', 'author', 'short_description', 'edition_author', 'edition_type',)


translator.register(ElectronLibrary, ElectronLibraryTranslationOptions)


class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(NewsCategory, NewsCategoryTranslationOptions)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description',)


translator.register(News, NewsTranslationOptions)


class HonestyTestCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(HonestyTestCategory, HonestyTestCategoryTranslationOptions)


class HonestyTestTranslationOptions(TranslationOptions):
    fields = ('question', 'advice',)


translator.register(HonestyTest, HonestyTestTranslationOptions)


class HonestyTestAnswerTranslationOptions(TranslationOptions):
    fields = ('answer',)


translator.register(HonestyTestAnswer, HonestyTestAnswerTranslationOptions)


class CorruptionRiskTranslationOptions(TranslationOptions):
    fields = ('name', 'short_desc', 'result')


translator.register(CorruptionRisk, CorruptionRiskTranslationOptions)


class CorruptionRiskMediaTranslationOptions(TranslationOptions):
    fields = ('filename',)


translator.register(CorruptionRiskMedia, CorruptionRiskMediaTranslationOptions)


class ProfessionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Profession, ProfessionTranslationOptions)


class ProfessionalEthicsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'case')


translator.register(ProfessionalEthics, ProfessionalEthicsTranslationOptions)


class ReportTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ReportType, ReportTypeTranslationOptions)


class AnnouncementCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(AnnouncementCategory, AnnouncementCategoryTranslationOptions)


class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


translator.register(Announcement, AnnouncementTranslationOptions)


class HandoutCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(HandoutCategory, HandoutCategoryTranslationOptions)


class HandoutTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Handout, HandoutTranslationOptions)
