from importlib.util import find_spec

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from health_check.views import HealthCheckView

health_check_checks = [
    "health_check.Database",
    "health_check.Storage",
    "health_check.contrib.psutil.Disk",
    "health_check.contrib.psutil.Memory",
]

if find_spec("celery"):
    health_check_checks.append("health_check.contrib.celery.Ping")

urlpatterns = [
    path(
        "health-check/",
        HealthCheckView.as_view(checks=health_check_checks),
        name="health_check",
    ),
    path("", include("yodaspeak.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
