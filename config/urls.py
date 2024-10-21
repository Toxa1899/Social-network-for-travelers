from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings

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


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
