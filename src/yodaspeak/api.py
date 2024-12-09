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


@api.post("/translate", response={200: TranslateResponse, 400: Message, 500: Message})
def translate(request, translate: TranslateRequest):
    sample = settings.TRANSLATE_SAMPLES.get(translate.text)
    if sample:
        return 200, {"translation": sample}

    try:
        response = translate_request(translate.text)
        return 200, {"translation": response.content}
    except Exception as e:
        return 400, {"message": f"Sorry, am I, as translate your message, I cannot. Error: {str(e)}"}
