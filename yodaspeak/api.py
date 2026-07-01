import logging

from django.conf import settings
from django.http import HttpRequest
from ninja import NinjaAPI, Schema

from .translate import TranslationError, translate_request

api = NinjaAPI()
logger = logging.getLogger(__name__)


class TranslateRequest(Schema):
    text: str


class TranslateResponse(Schema):
    translation: str


class Message(Schema):
    message: str


def get_sample_translation(text: str) -> str | None:
    sample_text = text[:100].casefold()
    for phrase, translation in settings.TRANSLATE_SAMPLES.items():
        if phrase.casefold() == sample_text:
            return translation
    return None


@api.post("/translate", response={200: TranslateResponse, 400: Message, 429: Message, 500: Message, 502: Message})
def translate(request: HttpRequest, translate: TranslateRequest):
    sample = get_sample_translation(translate.text)
    if sample:
        return 200, {"translation": sample}

    try:
        return 200, {"translation": translate_request(translate.text)}
    except TranslationError as exc:
        logger.warning("Translation request failed: %s", exc.message)
        return exc.status_code, {"message": exc.message}
    except Exception:
        logger.exception("Translation request failed")
        return 500, {"message": "Sorry, am I, as translate your message, I cannot."}
