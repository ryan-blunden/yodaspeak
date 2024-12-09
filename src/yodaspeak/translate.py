from typing import Callable

from django.conf import settings
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI()


def translate_request(phrase) -> Callable:
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

    response = client.chat.completions.create(
        messages=messages, model=settings.OPENAI_MODEL, temperature=0.7, max_tokens=500
    )
    return response.choices[0].message
