from django.contrib import admin
from .models import (Region, District,
                     AboutUs, Banner, StatisticYear,
                     RainbowStatistic, LinerStatistic,
                     QuarterlyStatistic)


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


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')
    list_display_links = ('id', 'title')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


@admin.register(StatisticYear)
class StatisticYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')
    list_display_links = ('id', 'year')


@admin.register(RainbowStatistic)
class RainbowStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'high', 'satisfactory', 'unsatisfactory')
    list_display_links = ('id', 'year')


@admin.register(LinerStatistic)
class LinerStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'name', 'percentage')
    list_display_links = ('id', 'year')


@admin.register(QuarterlyStatistic)
class QuarterlyStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'name', 'this_year', 'last_year')
    list_display_links = ('id', 'year')
    search_fields = ('name',)
    readonly_fields = ('this_year',)
