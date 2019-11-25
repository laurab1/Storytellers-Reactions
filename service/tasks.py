import requests

from flask import current_app
from service.extensions import celery
from service.models import Reaction, db

new_reacts = {}

@celery.task
def notify_reactions():
    '''
    Add a reaction to the Reactions database
    '''
    if new_reacts:
        requests.post(f'{app.config[STORIES_ENDPOINT]}/stories/react_upd', json=new_reacts)
        new_reacts = {}
    
    return 200


@celery.task
def remove_deleted(storyid):
    '''
    Removes reactions to a deleted story
    '''
    q =  Reaction.query.filter_by(story_id=storyid)
    for row in q:
        db.session.delete(row)
        db.session.commit()