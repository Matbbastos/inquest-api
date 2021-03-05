import unittest
import json

from api import app as APP


class TestHomeView(unittest.TestCase):
    """Tests the Home page, at route '/'."""

    def setUp(self):
        """Executes each time Pytest instances the class."""
        app = APP.test_client()
        self.response = app.get('/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_html_string_response(self):
        self.assertEqual({'status': 'Isso deu certo!'}, json.loads(self.response.data))

    def test_content_type(self):
        self.assertIn('application/json', self.response.content_type)
