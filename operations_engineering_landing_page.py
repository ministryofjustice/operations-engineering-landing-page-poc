"""operations-engineering-landing-page"""
import sys
import logging
from os import environ
from dotenv import dotenv_values

from landing_page_app.main.services.github_service import GithubService
from landing_page_app.main.scripts.github_script import GithubScript
from landing_page_app import create_app


def get_tokens():
    github_token = environ.get("GH_TOKEN")
    if not github_token:
        # Look for a local .env file
        github_token = dotenv_values(".env").get("GH_TOKEN")
        if not github_token:
            logging.error("Failed to find a GitHub Token")
            sys.exit(1)
    return github_token


def build_app():
    github_token = get_tokens()
    github_service = GithubService(github_token)
    github_script = GithubScript(github_service)
    return create_app(github_script)


# Gunicorn entry point, return the object without running it
def app():
    return build_app()


# Run Flask locally entry point for makefile and debugger
def run_app():
    flask_app = build_app()
    flask_app.run(port=4567)
    return flask_app


if __name__ == "__main__":
    run_app()
