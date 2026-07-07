from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, TestCase

from .translate import (
    TranslationError,
    _extract_provider_error,
    translate_request,
)
from .views import index


class ViewTests(SimpleTestCase):
    def test_index_page(self):
        request = RequestFactory().get("/")
        response = index(request)
        self.assertEqual(response.status_code, 200)


class TranslateApiTests(TestCase):
    @patch("yodaspeak.api.translate_request", return_value="Strong with the Force, you are.")
    def test_translate_returns_openai_translation(self, translate_request):
        response = self.client.post(
            "/api/translate",
            data='{"text":"You are strong with the Force."}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translation": "Strong with the Force, you are."})
        translate_request.assert_called_once_with("You are strong with the Force.")

    @patch("yodaspeak.api.translate_request", side_effect=RuntimeError("missing key"))
    def test_translate_returns_error_message_when_translation_fails(self, _translate_request):
        response = self.client.post(
            "/api/translate",
            data='{"text":"Translate this"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("Sorry, am I, as translate your message, I cannot.", response.json()["message"])

    @patch(
        "yodaspeak.api.translate_request",
        side_effect=TranslationError(
            "Could not finish the message because max_tokens or model output limit was reached.",
            502,
        ),
    )
    def test_translate_returns_provider_message_for_translation_error(self, _translate_request):
        response = self.client.post(
            "/api/translate",
            data='{"text":"ngrok ship is brilliant"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json(),
            {"message": "Could not finish the message because max_tokens or model output limit was reached."},
        )


class TranslateRequestTests(SimpleTestCase):
    def test_extract_provider_error_message_prefers_string_body(self):
        exc = SimpleNamespace(
            body='[ERR_NGROK_27202] No keys available for provider "groq".',
            message="Error code: 502",
        )

        self.assertEqual(
            _extract_provider_error(exc),
            '[ERR_NGROK_27202] No keys available for provider "groq".',
        )

    def test_extract_provider_error_message_falls_back_to_plain_message(self):
        exc = SimpleNamespace(message='[ERR_NGROK_27202] No keys available for provider "groq".')

        self.assertEqual(
            _extract_provider_error(exc),
            '[ERR_NGROK_27202] No keys available for provider "groq".',
        )

    @patch("yodaspeak.translate.client.chat.completions.create")
    def test_translate_request_returns_message_content(self, create):
        create.return_value = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Much to learn, you still have."),
                    finish_reason="stop",
                )
            ],
            usage=None,
        )

        self.assertEqual(translate_request("You still have much to learn."), "Much to learn, you still have.")
