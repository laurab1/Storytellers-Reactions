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
import json
from flask import request
from service.tasks import *


reactions = Blueprint('reactions', __name__)


@reactions.route('/users/<userid>/get_react', methods=['GET'])
def get_user_react(userid):
    '''
    Retrieves all the reactions from a given user
    Returns:
        200 -> User reactions retrieved successfully
        404 -> User not found
    '''
    
    q = Reaction.query.filter_by(reactor_id=userid)
            
    likes, dislikes = _compute_reacts(q)
           
    return jsonify({'likes':likes, 'dislikes':dislikes})        


@reactions.route('/stories/<storyid>/get_react', methods=['GET'])
def get_story_react(storyid):
    '''
    Retrieves all the reactions to a given story
    Returns:
        200 -> Story reactions retrieved successfully
        404 -> The requested story does not exist
        403 -> The requested story is a draft
        410 -> The requested story was previously deleted
    '''
    response, sid = _check_story(storyid)
    
    if response is not None:
        return response
    
    q = Reaction.query.filter_by(story_id=storyid)
    
    likes, dislikes = _compute_reacts(q)
           
    return jsonify({'likes':likes, 'dislikes':dislikes})


@reactions.route('/stories/<storyid>/react', methods=['POST'])
#@jwt_required
def post_story_react(storyid):
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
    response, sid = _check_story(storyid)
    
    if response is not None:
        return response
    
    # ERROR CHECK (payload)
    payload = request.get_json()
    
    # checks whether the payload is empty or ill-formed
    value = 'react' in payload
    
    if value is False:
        return jsonify(error='Reaction message must not be empty'), 400
    
    if payload['react'] != 'like' and payload['react'] != 'dislike':
        return jsonify(error='Reaction value must be \'like\' or \'dislike\''), 400
    
    # ERROR CHECK (user)
    userid = 1 # must be obtained from the token

    removed = False
    q = Reaction.query.filter_by(reactor_id=userid,
                                 story_id=sid).one_or_none()

    react = 1 if payload['react'] == 'like' else -1
    if q is None or react != q.reaction_val:
        if q is not None and react != q.reaction_val:
            # remove the old reaction if the new one has different value
            db.session.delete(q)
            db.session.commit()
            removed = True
        new_reaction = Reaction()
        new_reaction.reactor_id = userid
        new_reaction.story_id = sid
        new_reaction.reaction_val = react
        db.session.add(new_reaction)
        db.session.commit()
        db.session.refresh(new_reaction)
        # votes are notified asynchronously to the story service
        #notify_reaction.delay(current_user.id, storyid, react)
        message = 'Reaction registered' if not removed else 'Reaction updated'
        return jsonify(message=message)

    if react == 1:
        return jsonify(error='You\'ve already liked this story'), 400
    return jsonify(error='You\'ve already disliked this story'), 400


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

def _check_story(storyid):
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
        return jsonify(error='The story identifier must be an integer'), 400
    
    s = _story_stub(sid) # here we should call the Story service...
    
    # checks whether the story exists, if it is a draft, or if it was previously deleted
    if s is 0:
        return jsonify(error='The requested story does not exist'), 404
    if s is 2:
        remove_deleted.delay(storyid)
        return jsonify(error='Story ' + storyid + ' was deleted'), 410
    if s is 3:
        return jsonify(error='The requested story is a draft'), 403
    
    return None, sid


###############################################################################################

# Stupid stub function to emulate the Story service
def _story_stub(storyid):
    if storyid in range(1,3): # story ok
        return 1
    elif storyid in range(3,6): # deleted story
        return 2
    elif storyid in range(6,8): # draft story
        return 3
    else:
        return 0
    
    
#try:
#    data = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
#    return data['sub']
#except jwt.ExpiredSignatureError:
#    return 'Signature expired. Please log in again.'
#except jwt.InvalidTokenError:
#    return 'Invalid token. Please log in again.'