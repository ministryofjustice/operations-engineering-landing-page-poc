"""Flask App"""
import logging

from flask import Flask
from flask_cors import CORS
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader

from landing_page_app.main.views import (main, page_not_found, server_forbidden, unknown_server_error)

def create_app() -> Flask:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s : %(message)s',
    )
    app = Flask(__name__, instance_relative_config=True)

    # Config folder file mapping
    config = {
        "development": "landing_page_app.config.development"
    }

    # Set config file and logging level
    app.config.from_object(config["development"])
    app.logger.setLevel(logging.DEBUG)
    logging.info("Running in Development mode.")

    # Load sensitive settings from instance/config.py
    app.config.from_pyfile("config.py", silent=True)

    logging.info("App Setup")

    app.secret_key = app.config.get("APP_SECRET_KEY")

    app.register_blueprint(main)

    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("landing_page_app"),
            PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
        ]
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.register_error_handler(403, server_forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, unknown_server_error)

    # Security and Protection extenstions
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    logging.info("App Setup complete, running App...")

    return app
