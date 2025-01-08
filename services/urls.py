from django.urls import path
from .views import (
    OrganizationViewSet, TrainingViewSet, ElectronLibraryViewSet,
    NewsViewSet, HonestyViewSet, ConflictAlertViewSet,
    ProfessionalEthicsViewSet, OfficerAdviceViewSet, ViolationReportViewSet,
    TechnicalSupportViewSet
)

urlpatterns = [
    path('organization/', OrganizationViewSet.as_view({'get': 'organization_list'})),

    path('organization/category/', OrganizationViewSet.as_view({'get': 'organization_categories'})),


    path('training/', TrainingViewSet.as_view({'get': 'training_list'})),
    path('training/<int:pk>/', TrainingViewSet.as_view({'get': 'training'})),
    path('training/category/', TrainingViewSet.as_view({'get': 'training_category'})),

    path('electron/library/', ElectronLibraryViewSet.as_view({'get': 'electron_library_list'})),
    path('electron/library/category/', ElectronLibraryViewSet.as_view({'get': 'electron_library_category'})),

    path('news/', NewsViewSet.as_view({'get': 'news_list'})),
    path('news/<int:pk>/', NewsViewSet.as_view({'get': 'news'})),
    path('news/category/', NewsViewSet.as_view({'get': 'news_category'})),

    path('honesty/test/', HonestyViewSet.as_view({'get': 'honesty_test_list'})),
    path('honesty/test/<int:pk>/', HonestyViewSet.as_view({'get': 'honesty_test'})),
    path('honesty/answer/', HonestyViewSet.as_view({'get': 'honesty_test_answer'})),

    path('conflict/alert/',
         ConflictAlertViewSet.as_view({'post': 'create_conflict_alert', 'delete': 'delete_conflict_alert'})),
    path('conflict/alert/<int:pk>/', ConflictAlertViewSet.as_view({'get': 'conflict_alert'})),
    path('professional/', ProfessionalEthicsViewSet.as_view({'get': 'profession_list'})),
    path('professional/ethics/', ProfessionalEthicsViewSet.as_view({'get': 'professional_ethics_list'})),
    path('professional/ethics/<int:pk>/', ProfessionalEthicsViewSet.as_view({'get': 'professional_ethics'})),

    path('officer/advice/', OfficerAdviceViewSet.as_view({'post': 'create_officer_advice'})),
    path('officer/advice/', OfficerAdviceViewSet.as_view({'post': 'officer_advice_list'})),

    path('violation/report/', ViolationReportViewSet.as_view({'post': 'create_violation_report'})),
    path('violation/report/types/', ViolationReportViewSet.as_view({'post': 'report_types'})),

    path('technical/support/', TechnicalSupportViewSet.as_view({'post': 'create_technical_support'}))
]
