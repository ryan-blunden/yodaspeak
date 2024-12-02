from django.test import TestCase


class ViewTests(TestCase):
    def test_index_page(self):
        """Index page should respond with a success 200."""
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
