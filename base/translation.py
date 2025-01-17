from modeltranslation.translator import translator, TranslationOptions
from .models import Region, District, FAQ, AboutUs, Banner, LinerStatistic

class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description')


class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description')


class LinerStatisticTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Region, RegionTranslationOptions)
translator.register(District, DistrictTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
translator.register(AboutUs, AboutUsTranslationOptions)
translator.register(Banner, BannerTranslationOptions)
translator.register(LinerStatistic, LinerStatisticTranslationOptions)
