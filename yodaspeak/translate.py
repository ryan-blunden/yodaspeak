from django.conf import settings
from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class TranslationError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _extract_provider_error(exc: Exception) -> str:
    body = getattr(exc, "body", None)

    if isinstance(body, str):
        return body
    if isinstance(body, dict):
        return body.get("message", str(body))
    if body:
        return str(body)
    return getattr(exc, "message", str(exc))


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

    request_kwargs = {
        "model": settings.OPENAI_MODEL,
        "messages": messages,
    }
    try:
        response = client.chat.completions.create(**request_kwargs)
    except AuthenticationError as exc:
        raise TranslationError(f"Authentication failed: {_extract_provider_error(exc)}", 502) from exc
    except RateLimitError as exc:
        raise TranslationError(f"Rate limit reached: {_extract_provider_error(exc)}", 429) from exc
    except APIConnectionError as exc:
        raise TranslationError(f"Could not reach Provider: {_extract_provider_error(exc)}", 502) from exc
    except APIStatusError as exc:
        raise TranslationError(_extract_provider_error(exc), 502) from exc
    return response.choices[0].message.content.replace('"', "") or ""
