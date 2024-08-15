import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "")
    REDIS_HOST = os.getenv("REDIS_HOST", "")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass


app_config = dict(development=DevConfig, production=ProdConfig)
