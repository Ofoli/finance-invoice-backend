import os
import logging

from dotenv import load_dotenv
from flask import Flask

from ..config import app_config
from ..config.extensions import init_extensions

from .constants import LOGS_DIR, APP_LOGGER

load_dotenv()


def _create_logger(name: str, file_path: str) -> None:
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s")

    logs_dir: str = os.path.dirname(file_path)
    os.makedirs(logs_dir, exist_ok=True)

    logger: logging.Logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.FileHandler(file_path)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False


def _register_blueprints(app: Flask):
    from .users import users_bp
    from .auth import auth_bp
    from .clients import client_bp

    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(client_bp, url_prefix="/api/clients")


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    init_extensions(app)

    _create_logger(APP_LOGGER, file_path=os.path.join(LOGS_DIR, "syslog.log"))

    _register_blueprints(app)

    return app


app = create_app(os.environ["FLASK_ENV"])
