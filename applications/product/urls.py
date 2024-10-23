from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostModelViewSet, CommentModelViewSet

router = DefaultRouter()
router.register("comment", CommentModelViewSet)
router.register("", PostModelViewSet)


urlpatterns = [path("", include(router.urls))]
