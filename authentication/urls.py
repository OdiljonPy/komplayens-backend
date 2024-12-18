from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('otp/verify/', UserViewSet.as_view({'post': 'verify_otp'}), name='otp_verify'),
    path('otp/resend/', UserViewSet.as_view({'post': 'resend_otp'}), name='otp_resend'),
    path('me/', UserViewSet.as_view({'get': 'user_detail', 'patch': 'user_update'}), name='user_detail'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
]
