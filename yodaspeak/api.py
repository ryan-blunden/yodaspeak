import logging

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


@api.post("/translate", response={200: TranslateResponse, 400: Message, 429: Message, 500: Message, 502: Message})
def translate(request: HttpRequest, translate: TranslateRequest):
    try:
        return 200, {"translation": translate_request(translate.text)}
    except TranslationError as exc:
        logger.warning("Translation request failed: %s", exc.message)
        return exc.status_code, {"message": exc.message}
    except Exception as exc:
        logger.exception("Translation request failed")
        return 500, {"message": f"Sorry, am I, as translate your message, I cannot. ({exc})"}
