from django.urls import path
from .views import (RegionViewSet, DistrictViewSet, FAQViewSet,
                    AboutUsViewSet, CorruptionCaseViewSet, CorruptionRiskViewSet)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'}), name='regions_list'),
    path('region/<int:pk>/',
         RegionViewSet.as_view({'get': 'detail_'}), name='region_funcs'),
    path('districts/', DistrictViewSet.as_view({'get': 'list'}), name='districts_list'),
    path('district/<int:pk>/',
         DistrictViewSet.as_view({'get': 'detail_'}), name='district_funcs'),
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq_list'),
    path('faq/<int:pk>/',
         FAQViewSet.as_view({'get': 'detail_'}), name='faq_funcs'),
    path('about/', AboutUsViewSet.as_view({'get': 'last'}), name='last_about'),
    path('corruptioncase/', CorruptionCaseViewSet.as_view({'get': 'list'}), name='corruption_case_list'),
    path('corruptioncase/<int:pk>/',
         CorruptionCaseViewSet.as_view({'get': 'detail_'}), name='corruption_case_funcs'),
    path('corruptionrisk/', CorruptionRiskViewSet.as_view({'get': 'list'}), name='corruption_risk_list'),
    path('corruptionrisk/<int:pk>/',
         CorruptionRiskViewSet.as_view({'get': 'detail_'}), name='corruption_risk_funcs'),
]
