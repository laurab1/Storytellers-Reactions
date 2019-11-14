# -*- coding: utf-8 -*-

TESTING = True
DEBUG = True
SECRET_KEY = 'change me please'

USERS_ENDPOINT = 'localhost:5001'
STORIES_ENDPOINT = 'localhost:5002'
REACTIONS_ENDPOINT = 'localhost:5003'
SEARCH_ENDPOINT = 'localhost:5004'
AUTH_ENDPOINT = 'localhost:5005'

# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json']
