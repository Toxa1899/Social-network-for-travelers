from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostModelViewSet, CommentModelViewSet, MainViewSet

router = DefaultRouter()
router.register("feed", MainViewSet, basename="feed")
router.register("comment", CommentModelViewSet)
router.register("", PostModelViewSet)


urlpatterns = [path("", include(router.urls))]
