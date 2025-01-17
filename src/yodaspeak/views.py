from django.conf import settings
from django.shortcuts import render


def index(request):
    translate_samples = settings.TRANSLATE_SAMPLES
    return render(request, "yodaspeak/app.html", {"translate_samples": translate_samples})
