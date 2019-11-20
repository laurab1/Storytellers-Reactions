from flask import current_app

from service.extensions import celery
from service.models import Reaction, db


@celery.task
def notify_reaction(reactorid, storyid, react):
    '''
    Add a reaction to the Reactions database
    '''
    
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