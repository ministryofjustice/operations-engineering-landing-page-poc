import unittest
from unittest.mock import MagicMock

from landing_page_app.main.scripts.github_script import GithubScript
import landing_page_app

from landing_page_app.main.views import (
    handle_github_exception,
    page_not_found,
    server_forbidden,
    unknown_server_error,
    gateway_timeout,
)


class TestViews(unittest.TestCase):
    def setUp(self):
        self.github_script = MagicMock(GithubScript)
        self.app = landing_page_app.create_app(self.github_script)

    def test_index(self):
        response = self.app.test_client().get("index")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/index")

    def test_home(self):
        response = self.app.test_client().get("home")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/home")

    def test_default(self):
        response = self.app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/")

    def test_join_github_info_page(self):
        response = self.app.test_client().get("/join-github.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github.html")

    def test_join_github_form(self):
        response = self.app.test_client().get("/join-github-form.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form.html")

    def test_thank_you(self):
        response = self.app.test_client().get("/thank-you")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/thank-you")

    def test_handle_github_exception(self):
        with self.app.test_request_context():
            response = handle_github_exception("12345678")
            self.assertRegex(response, "There was an intenal error: 12345678")

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


class TestCompletedJoinGithubForm(unittest.TestCase):
    def setUp(self):
        self.form_data = {
            "gh_username": "some-username",
            "name": "some name",
            "email_address": "some@email.com",
            "access_moj_org": True,
            "access_as_org": True,
        }

        self.github_script = MagicMock(GithubScript)
        self.app = landing_page_app.create_app(self.github_script)

    def test_join_github_form(self):
        self.github_script.get_selected_organisations.return_value = "some-org"
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/thank-you")

    def test_join_github_form_with_incorrect_special_character_inputs(self):
        self.form_data["gh_username"] = "some!username"
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")
        self.form_data["gh_username"] = "some-username"

        self.form_data["email_address"] = "some!email!"
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")
        self.form_data["email_address"] = "some@email.com"

        self.form_data["name"] = "name1!"
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")
        self.form_data["name"] = "some name"

    def test_join_github_form_with_missing_username(self):
        self.form_data["gh_username"] = None
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

        self.form_data["gh_username"] = ""
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

    def test_join_github_form_with_missing_email_address(self):
        self.form_data["email_address"] = None
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

        self.form_data["email_address"] = ""
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

    def test_join_github_form_with_missing_name(self):
        self.form_data["name"] = None
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

        self.form_data["name"] = ""
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

    def test_join_github_form_with_missing_orgs(self):
        self.form_data["access_moj_org"] = None
        self.form_data["access_as_org"] = None
        response = self.app.test_client().post("/join-github-form", data=self.form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")

        form_data = {
            "gh_username": "some-username",
            "name": "some name",
            "email_address": "some@email.com"
        }
        response = self.app.test_client().post("/join-github-form", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/join-github-form")


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)