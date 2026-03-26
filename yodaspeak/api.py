from django.conf import settings
from ninja import NinjaAPI, Schema

from .translate import translate_request

api = NinjaAPI()


class TranslateRequest(Schema):
    text: str


class TranslateResponse(Schema):
    translation: str


class Message(Schema):
    message: str


def get_sample_translation(text: str) -> str | None:
    return settings.TRANSLATE_SAMPLES.get(text[:100])


@api.post("/translate", response={200: TranslateResponse, 400: Message})
def translate(request, translate: TranslateRequest):
    sample = get_sample_translation(translate.text)
    if sample:
        return 200, {"translation": sample}

    try:
        return 200, {"translation": translate_request(translate.text)}
    except Exception as exc:
        return 400, {"message": f"Sorry, am I, as translate your message, I cannot. Error: {exc}"}
