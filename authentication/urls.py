from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('me/', UserViewSet.as_view({'get': 'user_detail', 'patch': 'user_update'}), name='user_detail'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
]
