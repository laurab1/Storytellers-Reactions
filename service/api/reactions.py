import json
import requests
from flask import Blueprint
from service.extensions import db
from flask import current_app as app
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import abort
from service.models import db, Reaction
from requests.exceptions import Timeout
from flask import request
from service import errors
from service.tasks import reacts_lock, new_reacts, remove_deleted


reactions = Blueprint('reactions', __name__)

BP_ID = 0

@reactions.route('/users/<userid>/get_react', methods=['GET'])
def get_user_react(userid, func_id=2):
    '''
    Retrieves all the reactions from a given user
    Returns:
        200 -> User reactions retrieved successfully
        404 -> User not found
    '''
    
    # ERROR CHECK
    # Raises exception if the provided id is not an integer
    try:
        uid = int(userid)
    except ValueError:
        return errors.response(f'{BP_ID}{func_id}0')
    
    # Tries to retrieve the user from the User service
    try:
        resp = requests.get(f'{app.config["USERS_ENDPOINT"]}/user/{userid}',
                                        timeout=app.config['REQUESTS_TIMEOUT'],
                                        json=request.json)
    except Timeout:
        return jsonify({}), 500
    
    if resp.status_code == 404: # Not registered user
        return errors.response(f'{BP_ID}{func_id}1')
    
    # Retrieve reactions and compute them
    q = Reaction.query.filter_by(reactor_id=userid)
            
    likes, dislikes = _compute_reacts(q)
           
    return jsonify({'likes':likes, 'dislikes':dislikes})        


@reactions.route('/stories/<storyid>/get_react', methods=['GET'])
def get_story_react(storyid, func_id=0):
    '''
    Retrieves all the reactions to a given story
    Returns:
        200 -> Story reactions retrieved successfully
        404 -> The requested story does not exist
        403 -> The requested story is a draft
        410 -> The requested story was previously deleted
    '''
    # Checks
    response = _check_story(storyid, 'get')
    
    if response is not None:
        return response
    
    sid = int(storyid)
    q = Reaction.query.filter_by(story_id=storyid)
    
    # Compute reactions to the story
    likes, dislikes = _compute_reacts(q)
           
    return jsonify({'likes':likes, 'dislikes':dislikes})


@reactions.route('/stories/<storyid>/react', methods=['POST'])
@jwt_required
def post_story_react(storyid, func_id=1):
    '''
    Process react requests by users to a story

    Returns:
        200 -> Successful posting
        400 -> Reaction not posted (story already liked/disliked or ill-formed request)
        404 -> The requested story does not exist
        403 -> The requested story is a draft
        410 -> The requested story was previously deleted        
    '''
    # ERROR CHECK (story)
    response = _check_story(storyid, 'post')
    
    if response is not None:
        return response
    
    sid = int(storyid)
    
    # ERROR CHECK (payload)
    payload = request.get_json()
    
    # checks whether the payload is empty or ill-formed
    value = payload is not None and 'react' in payload
    
    if not value:
        return errors.response(f'{BP_ID}{func_id}3')
    
    if payload['react'] != 'like' and payload['react'] != 'dislike':
        return errors.response(f'{BP_ID}{func_id}2')
    
    # ERROR CHECK (user)
    # Here I just need if the user is actually registered
    current_user = get_jwt_identity()
    if current_user is None:
        errors.response(f'{BP_ID}{func_id}8')
    userid = current_user['user_id']

    removed = False
    q = Reaction.query.filter_by(reactor_id=userid,
                                 story_id=sid).one_or_none()

    react = 1 if payload['react'] == 'like' else -1
    if q is None or react != q.reaction_val:
        if q is not None and react != q.reaction_val:
            # Remove the old reaction if the new one has different value
            tmp_like = 1*react
            tmp_dislike = -1*react
            db.session.delete(q)
            db.session.commit()
            removed = True
        new_reaction = Reaction()
        new_reaction.reactor_id = userid
        new_reaction.story_id = sid
        new_reaction.reaction_val = react
        if not removed:
            if react == 1:
                tmp_like = 1
                tmp_dislike = 0
            else:
                tmp_like = 0
                tmp_dislike = 1

        db.session.add(new_reaction)
        db.session.commit()
        db.session.refresh(new_reaction)

        # Updating the dictionary of the reactions to be sent to the
        # stories endpoint
        with reacts_lock:
            if not storyid in new_reacts:
                new_reacts[storyid] = {'likes': 0, 'dislikes': 0 }
            new_reacts[storyid]['likes'] += tmp_like
            new_reacts[storyid]['dislikes'] += tmp_dislike
            
        message = 'Reaction registered' if not removed else 'Reaction updated'
        return jsonify(message=message)

    if react == 1:
        return errors.response(f'{BP_ID}{func_id}0')
    return errors.response(f'{BP_ID}{func_id}1')


###################################### UTILITY FUNCTIONS ######################################

def _compute_reacts(q):
    '''
    Computes the number of likes/dislikes for a given story or a given user
    
    Returns:
        likes, dislikes -> the number of the likes/dislikes to the story identified by storyid or from the user identified by userid
    '''
    likes = 0
    dislikes = 0
    for row in q:
        if row.reaction_val == 1:
            likes += 1
        else:
            dislikes += 1
    return likes, dislikes

def _check_story(storyid, method):
    '''
    Checks if a story exists, if it is deleted or a draft
    
    Returns:
        400 -> Story identifier is not an integer
        404 -> The requested story does not exist
        403 -> The requested story is a draft
        410 -> The requested story was previously deleted
        None -> The story exists
    '''
    try:
        sid = int(storyid)
    except ValueError:
        if method == 'get':
            return errors.response(f'{BP_ID}30')
        else:
            return errors.response(f'{BP_ID}14')
    
    try:
        resp = requests.get(f'{app.config["STORIES_ENDPOINT"]}/stories/{storyid}',
                                        timeout=app.config['REQUESTS_TIMEOUT'],
                                        json=request.json)
    except Timeout:
        return jsonify({}), 500
    
    # checks whether the story exists, if it is a draft, or if it was previously deleted
    if resp.status_code == 404: # the story does not exists
        if method == 'get':
            return errors.response(f'{BP_ID}32')
        else:
            return errors.response(f'{BP_ID}16')
    if resp.status_code == 410:
        remove_deleted.delay(storyid)
        if method == 'get':
            return errors.response(f'{BP_ID}33')
        else:
            return errors.response(f'{BP_ID}17')
    if resp.status_code == 403:
        if method == 'get':
            return errors.response(f'{BP_ID}31')
        else:
            return errors.response(f'{BP_ID}15')
    
    return None
