from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostModelViewSet,
    MainViewSet,
    DisablePost,
    PostLiftSettingsModelViewSet,
    LiftLogModelViewSet,
)

router = DefaultRouter()
router.register("feed", MainViewSet, basename="feed")
router.register("lift", PostLiftSettingsModelViewSet, basename="lift")
router.register("lift-log", LiftLogModelViewSet, basename="lift-log")

router.register("", PostModelViewSet, basename="posts")


urlpatterns = [
    path("", include(router.urls)),
    path("disable/<int:pk>/", DisablePost.as_view()),
]
