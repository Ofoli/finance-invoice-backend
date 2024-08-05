import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass


app_config = dict(development=DevConfig, production=ProdConfig)
