from flask import Blueprint
from service.extensions import db
from flask import current_app as app
from flask import jsonify

reactions = Blueprint('reactions', __name__)


@reactions.route('/stories/<storyid>/react', methods=['POST'])
def post_story_react():
    '''
    Process react requests by users to a story

    Returns:
        200 -> Successful posting
        400 -> Reaction not posted
    '''
    pass
