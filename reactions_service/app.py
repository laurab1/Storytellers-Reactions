import datetime as dt

from flask import Flask

from flask_bootstrap import Bootstrap

#from monolith import celeryapp
#from monolith.auth import login_manager
from reactions_service.database import db


def create_app(test=False, database='sqlite:///reactions.db',
               login_disabled=False):
    app = Flask(__name__)
    Bootstrap(app)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKED'] = 'redis://localhost:6379/0'

    app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(minutes=120)
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['LOGIN_DISABLED'] = login_disabled
    if test:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CELERY_ALWAYS_EAGER'] = True

    # initialize Celery
    #celery = celeryapp.create_celery_app(app)
    #celeryapp.celery = celery

    db.init_app(app)
    #login_manager.init_app(app)
    #login_manager.login_view = '/login'
    db.create_all(app=app)

    # Required to avoid circular dependencies
    #from reactions_service.views import blueprints
    #for bp in blueprints:
    #    app.register_blueprint(bp)
    #    bp.app = app

    #from monolith.views import errors
    #app.register_error_handler(400, errors.bad_request)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
