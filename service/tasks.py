from flask import current_app

from gateway.extensions import celery


@celery.task
def request_signup():
    return 200
