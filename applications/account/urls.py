from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ChangePasswordAPIView, DeleteAccountAPIView, RegisterAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path(
        "change_password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("refresh", TokenRefreshView.as_view()),
    path(
        "delete/",
        DeleteAccountAPIView.as_view(),
        name="delete-account",
    ),
]
