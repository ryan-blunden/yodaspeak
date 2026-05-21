import logging

from django.conf import settings
from django.http import HttpRequest
from ninja import NinjaAPI, Schema

from .translate import translate_request

api = NinjaAPI()
logger = logging.getLogger(__name__)


class TranslateRequest(Schema):
    text: str


class TranslateResponse(Schema):
    translation: str


class Message(Schema):
    message: str


def get_sample_translation(text: str) -> str | None:
    return settings.TRANSLATE_SAMPLES.get(text[:100])


@api.post("/translate", response={200: TranslateResponse, 400: Message, 500: Message})
def translate(request: HttpRequest, translate: TranslateRequest):
    sample = get_sample_translation(translate.text)
    if sample:
        return 200, {"translation": sample}

    try:
        return 200, {"translation": translate_request(translate.text)}
    except Exception:
        logger.exception("Translation request failed")
        return 500, {"message": "Sorry, am I, as translate your message, I cannot."}
