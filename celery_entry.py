# -*- coding: utf-8 -*-
from service.app import create_app, create_celery

app = create_app(config='service/config.py')
celery = create_celery(app)
celery.start()
