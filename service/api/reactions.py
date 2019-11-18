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
def post_story_react():
    '''
    Process react requests by users to a story

    Returns:
        200 -> Successful posting
        400 -> Reaction not posted
    '''
    pass
