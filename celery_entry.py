# -*- coding: utf-8 -*-
from service.app import create_app, create_celery
from service.tasks import notify_reactions

app = create_app(config='service/config.py')
celery = create_celery(app)

POLLING_RATE = 1.0

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #gather from story microservice
    sender.add_periodic_task(POLLING_RATE, notify_reactions.s(), name='reactions-microservice')

celery.start()
