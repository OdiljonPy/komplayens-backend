from django.urls import path
from .views import (
    RegionViewSet, DistrictViewSet, FAQViewSet,
    AboutUsViewSet
)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'}), name='regions_list'),
    path('region/<int:pk>/', DistrictViewSet.as_view({'get': 'list'}), name='districts_list'),
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq_list'),
    path('about/', AboutUsViewSet.as_view({'get': 'last'}), name='last_about')
]
