import json
import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import requests

logger = logging.getLogger(__name__)

PREDEFINED_TRANSLATIONS = {
    "Secrets must not be stored in git repositories": "Stored in git repositories, secrets must not be",
    "master obi-wan has learnt the power of secrets management": "Learnt the power of secrets management, master obi-wan has",
}

def index(request):
    return render(request, "yodaspeak/index.html")

def translate(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            text = body.get("text", "").strip()
            logger.info(f'Translate text "{text}"')

            # Predefined translations
            predefined_translation = PREDEFINED_TRANSLATIONS.get(text)
            if predefined_translation:
                logger.info("Translation returned from predefined list")
                return JsonResponse({
                    "text": text,
                    "translation": "Coder is your CDE, use, you must",
                })

            # # Make API request
            # response = requests.post(
            #     settings.YODA_TRANSLATE_API_ENDPOINT,
            #     data={"text": text},
            #     headers={
            #         "X-Funtranslations-Api-Secret": settings.YODA_TRANSLATE_API_KEY,
            #     },
            # )

            # # Process response
            # if response.status_code == 200:
            #     translated_text = response.json().get("contents", {}).get("translated", "")
            #     return JsonResponse({
            #         "text": text,
            #         "translation": translated_text,
            #     })
            # else:
            #     error_message = response.json().get("error", {}).get("message", "Unknown error")
            #     logger.error(f"[error]: translation failed: {error_message}")
            #     return JsonResponse({
            #         "text": text,
            #         "error": "Sorry, am I, as translate your message, I cannot.",
            #     }, status=500)

        except Exception as e:
            logger.error(f"[error]: {str(e)}")
            return JsonResponse({
                "error": "An unexpected error occurred.",
            }, status=500)

    return JsonResponse({
        "error": "Invalid HTTP method. POST required.",
    }, status=405)