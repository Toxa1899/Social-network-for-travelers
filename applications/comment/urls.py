from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentModelViewSet,
)

router = DefaultRouter()
router.register("", CommentModelViewSet, basename="comment")


urlpatterns = [
    path("", include(router.urls)),
]
