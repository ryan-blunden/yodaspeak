from django.conf import settings
from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam


class TranslationError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


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
        response = client.chat.completions.create(**request_kwargs)
    except AuthenticationError as exc:
        raise TranslationError("OpenAI authentication failed. Check the configured API key.", 502) from exc
    except RateLimitError as exc:
        raise TranslationError("OpenAI rate limit reached. Try again shortly.", 429) from exc
    except APIConnectionError as exc:
        raise TranslationError("Could not reach OpenAI. Try again shortly.", 502) from exc
    except APIStatusError as exc:
        message = exc.message or "OpenAI request failed."
        raise TranslationError(message, 502) from exc
    return response.choices[0].message.content or ""
