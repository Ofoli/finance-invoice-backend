from flask import Flask

from redis import Redis
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()


def _init_redis(app: Flask) -> None:
    app.extensions["redis"] = Redis(
        host=app.config["REDIS_HOST"], db=1, decode_responses=True
    )


def init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    _init_redis(app)
