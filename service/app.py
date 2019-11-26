# -*- coding: utf-8 -*-

from celery import Celery
from flask import Flask

from service.extensions import db, celery
from service.api.reactions import reactions
from service.models import db as md

from flask_jwt_extended import JWTManager

__all__ = ('create_app', 'create_celery')

# Import blueprints and insert in the list
BLUEPRINTS = (reactions,)


def create_app(config=None, app_name='reactions', blueprints=None):
    app = Flask(app_name)

    if config:
        app.config.from_pyfile(config)

    md.init_app(app)
    try:
        md.create_all(app=app)
    except Exception as e:
        print("DB already existed")

    jwt = JWTManager(app)

    if blueprints is None:
        blueprints = BLUEPRINTS

    create_celery(app)
    build_blueprints(app, blueprints)
    db.init_app(app)
    try:
        db.init_all(app=app)
    except Exception as e:
        print("DB already existed")

    celery.config_from_object(app.config)

    return app


def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def build_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
