from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('me/', UserViewSet.as_view({'get': 'user_detail', 'patch': 'user_update'}), name='user_detail'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
    path('password/recovery/', UserViewSet.as_view({'post': 'password_recovery'}), name='password_recovery'),
]
