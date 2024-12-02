from ninja import NinjaAPI, Schema

api = NinjaAPI()


class TranslateRequest(Schema):
    text: str


class TranslateResponse(Schema):
    text: str
    translation: str


@api.post("/translate", response=TranslateResponse)
def translate(request, reqeust: TranslateRequest):
    return {
        "text": "sdf",
        "translation": "Coder is your CDE, use, you must",
    }
