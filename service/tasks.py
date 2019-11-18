from flask import current_app

from service.extensions import celery


@celery.task
def request_signup():
    return 200
