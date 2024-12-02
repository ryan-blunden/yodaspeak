import json
import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import requests

logger = logging.getLogger(__name__)

PREDEFINED_TRANSLATIONS = {
    "Docker Compose is an essential local development tool.": "An essential tool for local development, Docker Compose is.",
    "Cloud Development Environments are the future.": "The future, Cloud Development Environments are.",
    "Running Docker inside your Coder workspace is eASY with EnvBox": "Easy it is to run Docker inside your Coder workspace, with EnvBox.",
}


def index(request):
    return render(request, "yodaspeak/app.html")


def translate(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            text = body.get("text", "").strip()
            logger.info(f'Translate text "{text}"')

            # Predefined translations
            predefined_translation = PREDEFINED_TRANSLATIONS.get(text)
            if predefined_translation:
                return JsonResponse(
                    {
                        "text": text,
                        "translation": "Coder is your CDE, use, you must",
                    }
                )

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
            return JsonResponse(
                {
                    "error": "An unexpected error occurred.",
                },
                status=500,
            )

    return JsonResponse(
        {
            "error": "Invalid HTTP method. POST required.",
        },
        status=405,
    )
