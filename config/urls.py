from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from health_check.views import HealthCheckView

urlpatterns = [
    path("health-check/", HealthCheckView.as_view(), name="health_check"),
    path("", include("yodaspeak.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
