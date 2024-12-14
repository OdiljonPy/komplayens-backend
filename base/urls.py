from django.urls import path
from .views import (RegionViewSet, DistrictViewSet, FAQViewSet,
                    AboutUsViewSet, CorruptionCaseViewSet, CorruptionRiskViewSet)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list', 'post': 'create'}), name='regions_list'),
    path('region/<int:pk>/',
         RegionViewSet.as_view({'get': 'detail_', 'patch': 'update', 'delete': 'delete'}),
         name='region_funcs'),
    path('districts/', DistrictViewSet.as_view({'get': 'list', 'post': 'create'}), name='districts_list'),
    path('district/<int:pk>/',
         DistrictViewSet.as_view({'get': 'detail_', 'patch': 'update', 'delete': 'delete'}),
         name='district_funcs'),
    path('faqs/', FAQViewSet.as_view({'get': 'list', 'post': 'create'}), name='faq_list'),
    path('faq/<int:pk>/',
         FAQViewSet.as_view({'get': 'detail_', 'patch': 'update', 'delete': 'delete'}),
         name='faq_funcs'),
    path('about/', AboutUsViewSet.as_view({'get': 'last', 'post': 'create'}), name='last_about'),
    path('about/<int:pk>/', AboutUsViewSet.as_view({'patch': 'update', 'delete': 'delete'}),
         name='about_funcs'),
    path('corruptioncase/', CorruptionCaseViewSet.as_view({'get': 'list', 'post': 'create'}), name='corruption_case_list'),
    path('corruptioncase/<int:pk>/',
         CorruptionCaseViewSet.as_view({'get': 'detail_', 'patch': 'update', 'delete': 'delete'}),
         name='corruption_case_funcs'),
    path('corruptionrisk/', CorruptionRiskViewSet.as_view({'get': 'list', 'post': 'create'}), name='corruption_risk_list'),
    path('corruptionrisk/<int:pk>/',
         CorruptionRiskViewSet.as_view({'get': 'detail_', 'patch': 'update', 'delete': 'delete'}),
         name='corruption_risk_funcs'),
]
