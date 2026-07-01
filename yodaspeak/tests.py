from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, TestCase

from .translate import TranslationError, translate_request
from .views import index


class ViewTests(SimpleTestCase):
    def test_index_page(self):
        request = RequestFactory().get("/")
        response = index(request)
        self.assertEqual(response.status_code, 200)


class TranslateApiTests(TestCase):
    @patch("yodaspeak.api.settings.TRANSLATE_SAMPLES", {"Hello there": "There hello, hmm?"})
    def test_translate_returns_sample_when_available(self):
        response = self.client.post(
            "/api/translate",
            data='{"text":"Hello there"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translation": "There hello, hmm?"})

    @patch("yodaspeak.api.settings.TRANSLATE_SAMPLES", {"Hello there": "There hello, hmm?"})
    def test_translate_returns_sample_case_insensitively(self):
        response = self.client.post(
            "/api/translate",
            data='{"text":"hello THERE"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translation": "There hello, hmm?"})

    @patch("yodaspeak.api.translate_request", return_value="Strong with the Force, you are.")
    @patch("yodaspeak.api.settings.TRANSLATE_SAMPLES", {})
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
    @patch("yodaspeak.api.settings.TRANSLATE_SAMPLES", {})
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
    @patch("yodaspeak.api.settings.TRANSLATE_SAMPLES", {})
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
