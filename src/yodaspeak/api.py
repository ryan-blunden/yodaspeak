from ninja import NinjaAPI, Schema

PREDEFINED_TRANSLATIONS = {
    "Docker Compose is an essential local development tool": "An essential tool for local development, Docker Compose is.",
    "Cloud Development Environments are the future": "The future, Cloud Development Environments are.",
    "Running Docker inside your Coder workspace is easy with EnvBox": "Easy it is to run Docker inside your Coder workspace, with EnvBox.",
}

api = NinjaAPI()


class TranslateRequest(Schema):
    text: str


class TranslateResponse(Schema):
    translation: str


class Message(Schema):
    message: str


@api.post("/translate", response={200: TranslateResponse, 400: Message, 500: Message})
def translate(request, translate: TranslateRequest):
    predefined_translation = PREDEFINED_TRANSLATIONS.get(translate.text)
    if predefined_translation:
        return 200, {"translation": predefined_translation}
    else:
        return 400, {"message": "Sorry, am I, as translate your message, I cannot."}
