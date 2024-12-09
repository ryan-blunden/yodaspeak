from django.urls import path

from yodaspeak import views

from .api import api

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", api.urls),
]
