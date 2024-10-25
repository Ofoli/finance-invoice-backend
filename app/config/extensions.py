from flask import Flask

from redis import Redis
from celery import Celery
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mailman import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.config import celery_task_config


ma = Marshmallow()
mail = Mail()
migrate = Migrate()
db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def _init_redis(app: Flask) -> None:
    app.extensions["redis"] = Redis(host=app.config["REDIS_HOST"], db=1, decode_responses=True)


def _init_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.config_from_object(celery_task_config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.extensions["celery"] = celery

    return celery


def init_extensions(app: Flask) -> None:
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    _init_redis(app)
    _init_celery(app)
