from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Social-network-for-travelers",
        default_version="v1",
        description="",
        contact=openapi.Contact(email=""),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/account/", include("applications.account.urls")),
    path("swagger/", schema_view.with_ui("swagger")),
]
