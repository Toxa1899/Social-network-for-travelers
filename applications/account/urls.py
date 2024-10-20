from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ChangePasswordAPIView, DeleteAccountAPIView, RegisterAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("change_password/", ChangePasswordAPIView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("delete/", DeleteAccountAPIView.as_view(), name="delete-account"),
]
