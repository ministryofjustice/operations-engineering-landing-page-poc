import unittest
from unittest.mock import MagicMock

import landing_page_app
from landing_page_app import GithubScript
from landing_page_app.main.middleware.error_handler import gateway_timeout, handle_github_exception, page_not_found, \
    server_forbidden, unknown_server_error


class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.github_script = MagicMock(GithubScript)
        self.app = landing_page_app.create_app(self.github_script, False)

    def test_handle_github_exception(self):
        with self.app.test_request_context():
            response = handle_github_exception("12345678")
            self.assertRegex(response, "12345678")

    def test_page_not_found(self):
        with self.app.test_request_context():
            response = page_not_found("some-error")
            self.assertEqual(response[1], 404)

    def test_server_forbidden(self):
        with self.app.test_request_context():
            response = server_forbidden("some-error")
            self.assertEqual(response[1], 403)

    def test_unknown_server_error(self):
        with self.app.test_request_context():
            response = unknown_server_error("some-error")
            self.assertEqual(response[1], 500)

    def test_gateway_timeout(self):
        with self.app.test_request_context():
            response = gateway_timeout("some-error")
            self.assertEqual(response[1], 504)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
