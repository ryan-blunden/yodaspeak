from django.conf import settings
from openai import OpenAI
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
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content or ""
