from django.urls import path
from .views import (
    RegionViewSet, DistrictViewSet,
    AboutUsViewSet, BannerViewSet, StatisticsViewSet
)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'}), name='regions_list'),
    path('region/<int:pk>/', DistrictViewSet.as_view({'get': 'list'}), name='districts_list'),
    path('about/', AboutUsViewSet.as_view({'get': 'last'}), name='last_about'),
    path('banner/', BannerViewSet.as_view({'get': 'banner_list'}), name='banners_list'),
    path('statistic/year/', StatisticsViewSet.as_view({'get': 'statistic_year'}), name='statistic_year'),
    path('statistic/', StatisticsViewSet.as_view({'get': 'statistics'}), name='statistics'),
    path('statistic/quarterly/', StatisticsViewSet.as_view({'get': 'quarterly_statistics'}), name='quarterly_statistic'),
]
