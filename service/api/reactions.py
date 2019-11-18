from flask import Blueprint
from service.extensions import db
from flask import current_app as app
from flask import jsonify

reactions = Blueprint('reactions', __name__)


@reactions.route('/users/{userid}/get_react', methods=['GET'])
def get_user_react():
    '''
    Retrieves all reactions from a given user
    Returns:
        200 -> User reactions retrieved successfully
        404 -> User not found
    '''
    pass


@reactions.route('/stories/{storyid}/get_react', methods=['GET'])
def get_story_react():
    '''
    Retrieves all reactions to a given story
    Returns:
        200 -> Story reactions retrieved successfully
        404 -> Story not found
    '''
    pass


@reactions.route('/stories/<storyid>/react', methods=['POST'])
@jwt_required
def post_story_react():
    '''
    Process react requests by users to a story

    Returns:
        200 -> Successful posting
        400 -> Reaction not posted
    '''
    s = # get story from Story service
    
    if s is None:
        abort(404, f'The requested story does not exist')
    if s.deleted:
        abort(410, f'Story {storyid} was deleted')
    if s.is_draft:
        abort(403, f'The requested story is a draft')
        
    user_id = # get user from auth
    
    # check auth token?

    q = Reaction.query.filter_by(reactor_id=user_id,
                                 story_id=storyid).one_or_none()

    react = 1 if 'like' in request.form else -1
    if q is None or react != q.reaction_val:
        if q is not None and react != q.reaction_val:
            # remove the old reaction if the new one has different value
            if q.marked:
                print(current_user.id)
                remove_reaction.delay(storyid, q.reaction_val)
                removed = True
            db.session.delete(q)
            db.session.commit()
        new_reaction = Reaction()
        new_reaction.reactor_id = current_user.id
        new_reaction.story_id = storyid
        new_reaction.reaction_val = react
        db.session.add(new_reaction)
        db.session.commit()
        db.session.refresh(new_reaction)
        # votes are registered asynchronously by celery tasks
        add_reaction.delay(current_user.id, storyid, react)
        message = 'Reaction registered' if not removed else 'Reaction updated'
        return jsonify(message=message)

    if react == 1:
        return jsonify(error='You\'ve already liked this story'), 400
    return jsonify(error='You\'ve already disliked this story'), 400
