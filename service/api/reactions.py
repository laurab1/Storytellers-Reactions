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
        404 -> Story not found
    '''
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
        400 -> Reaction not posted
    '''
    try:
        sid = int(storyid)
    except ValueError:
        return jsonify(error='The story identifier must be an integer'), 400
    
    s = _story_stub(sid) # here we should call the Story service...
    
    # check whether the story exists, if it is a draft, or if it was previously deleted
    if s is 0:
        return jsonify(error='The requested story does not exist'), 404
    if s is 2:
        return jsonify(error='Story {storyid} was deleted'), 410
    if s is 3:
        return jsonify(error='The requested story is a draft'), 403
    
    #try:
    #    data = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
    #    return data['sub']
    #except jwt.ExpiredSignatureError:
    #    return 'Signature expired. Please log in again.'
    #except jwt.InvalidTokenError:
    #    return 'Invalid token. Please log in again.'
    
    userid = 1 # must be obtained from the token

    q = Reaction.query.filter_by(reactor_id=userid,
                                 story_id=sid).one_or_none()
    
    payload = request.get_json()
    removed = False

    react = 1 if payload['react'] == 'like' else -1
    if q is None or react != q.reaction_val:
        if q is not None and react != q.reaction_val:
            # remove the old reaction if the new one has different value
            if q.marked:
                #remove_reaction.delay(storyid, q.reaction_val)
                removed = True
            db.session.delete(q)
            db.session.commit()
        new_reaction = Reaction()
        new_reaction.reactor_id = userid
        new_reaction.story_id = sid
        new_reaction.reaction_val = react
        db.session.add(new_reaction)
        db.session.commit()
        db.session.refresh(new_reaction)
        # votes are registered asynchronously by celery tasks
        #add_reaction.delay(current_user.id, storyid, react)
        message = 'Reaction registered' if not removed else 'Reaction updated'
        return jsonify(message=message)

    if react == 1:
        return jsonify(error='You\'ve already liked this story'), 400
    return jsonify(error='You\'ve already disliked this story'), 400

# A simple utility function to compute likes and dislikes
def _compute_reacts(q):
    likes = 0
    dislikes = 0
    for row in q:
        if row.reaction_val == 1:
            likes += 1
        else:
            dislikes += 1
    return likes, dislikes


###################################################################################
# Stupid stub function to emulate the Story service

def _story_stub(storyid):
    if storyid in range(1,3):
        return 1
    elif storyid in range(3,6):
        return 2
    elif storyid in range(6,8):
        return 3
    else:
        return 0