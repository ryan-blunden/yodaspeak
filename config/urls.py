from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from health_check import urls as health_check_urls

urlpatterns = [
    path("health-check/", include(health_check_urls)),
    path("", include("yodaspeak.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
