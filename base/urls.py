from django.urls import path
from .views import (RegionViewSet, DistrictViewSet, FAQViewSet,
                    AboutUsViewSet, CorruptionCaseViewSet, CorruptionRiskViewSet)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'}), name='regions_list'),
    path('districts/<int:pk>/', DistrictViewSet.as_view({'get': 'list'}), name='districts_list'),
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq_list'),
    path('about/', AboutUsViewSet.as_view({'get': 'last'}), name='last_about'),
    path('corruptioncase/', CorruptionCaseViewSet.as_view({'get': 'list'}), name='corruption_case_list'),
    path('corruptioncase/<int:pk>/',
         CorruptionCaseViewSet.as_view({'get': 'detail_'}), name='corruption_case_funcs'),
    path('corruptionrisk/', CorruptionRiskViewSet.as_view({'get': 'list'}), name='corruption_risk_list'),
    path('corruptionrisk/<int:pk>/',
         CorruptionRiskViewSet.as_view({'get': 'detail_'}), name='corruption_risk_funcs'),
]
