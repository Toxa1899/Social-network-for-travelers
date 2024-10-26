from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountriesModelViewSet, CountriesAllModelViewSet

router = DefaultRouter()


router.register("all", CountriesAllModelViewSet, basename="countries_all")
router.register("", CountriesModelViewSet, basename="countries")

urlpatterns = [
    path("", include(router.urls)),
]
