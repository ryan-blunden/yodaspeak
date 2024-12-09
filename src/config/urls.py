from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from health_check import urls as health_check_urls

urlpatterns = [
    path("health-check/", include(health_check_urls)),
    path("", include("yodaspeak.urls")),
    path("admin/", admin.site.urls),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
