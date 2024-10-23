from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ChangePasswordAPIView,
    DeleteAccountAPIView,
    RegisterAPIView,
    BlockedUserViewSet,
    UserViewSet,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("blocked-user", BlockedUserViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
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
