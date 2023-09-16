from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegistrationApiView, UserOnlineStatusApiView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("registration/", RegistrationApiView.as_view(), name="registration"),

    path("online_status/<int:user_id>/", UserOnlineStatusApiView.as_view(), name="online-status"),
]

app_name = "users"
