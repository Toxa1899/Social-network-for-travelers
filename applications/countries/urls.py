from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountriesModelViewSet


router = DefaultRouter()
router.register("", CountriesModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
