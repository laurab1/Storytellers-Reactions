import requests

from flask import current_app as app
from service.extensions import celery
from service.models import Reaction, db
import redis
import json


@celery.task
def notify_reactions():
    '''
    Add a reaction to the Reactions database
    '''
    r = redis.Redis.from_url(app.config['REDIS_URL'])
    new_reacts = r.get('new_reacts')
    if new_reacts:
        new_reacts = json.loads(new_reacts.decode('utf-8'))
        requests.post(f'{app.config["STORIES_ENDPOINT"]}/stories/react_upd', json=new_reacts)
        new_reacts = r.delete('new_reacts')


@celery.task
def remove_deleted(storyid):
    '''
    Removes reactions to a deleted story
    '''
    q =  Reaction.query.filter_by(story_id=storyid)
    for row in q:
        db.session.delete(row)
        db.session.commit()
