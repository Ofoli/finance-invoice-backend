import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    PORT = int(os.getenv("APP_PORT", 5000))
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "")
    REDIS_HOST = os.getenv("REDIS_HOST", "")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = os.environ.get("MAIL_PORT", "")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass


app_config = dict(development=DevConfig, production=ProdConfig)
