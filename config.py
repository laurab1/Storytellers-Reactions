# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = 'change me please'
#JWT_TOKEN_LOCATION = 'headers'

# Upstream requests timeout in seconds
REQUESTS_TIMEOUT = 0.33

USERS_ENDPOINT = 'localhost:5001'
STORIES_ENDPOINT = 'localhost:5002'
REACTIONS_ENDPOINT = 'localhost:5003'
SEARCH_ENDPOINT = 'localhost:5004'
AUTH_ENDPOINT = 'localhost:5005'
SQLALCHEMY_DATABASE_URI = 'sqlite:///reactions.db'

# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json']
