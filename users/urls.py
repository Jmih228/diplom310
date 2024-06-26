from django.urls import path
from users.apps import UsersConfig
from users.views import (UserCreateAPIView,
                         UserUpdateAPIView,
                         UserProfileAPIView,
                         SMSCodeView,)


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('get_sms_code/', SMSCodeView.as_view(), name='sms_code_auth'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('profile_update/<int:pk>/', UserUpdateAPIView.as_view(), name='profile_update')
]
