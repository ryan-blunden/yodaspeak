from django.conf import settings
from openai import BadRequestError, OpenAI
from openai.types.chat import ChatCompletionMessageParam


def translate_request(phrase: str) -> str:
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": settings.YODASPEAK_PROMPT,
        },
        {
            "role": "user",
            "content": phrase,
        },
    ]

    client = OpenAI(api_key=settings.OPENAI_API_KEY or None)
    request_kwargs = {
        "model": settings.OPENAI_MODEL,
        "messages": messages,
    }
    try:
        response = client.chat.completions.create(
            **request_kwargs,
            max_completion_tokens=500,
        )
    except BadRequestError as exc:
        # Some older chat-completions models only support max_tokens.
        if "max_completion_tokens" not in str(exc):
            raise
        response = client.chat.completions.create(
            **request_kwargs,
            max_tokens=500,
        )
    return response.choices[0].message.content or ""
