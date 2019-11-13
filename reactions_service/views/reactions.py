from flask import jsonify
from flask import current_app as app
from flask_login import login_required

from reactions_service.database import db

from flakon import SwaggerBlueprint

reactions = SwaggerBlueprint('swagger', spec='reactions_specs.yml')

@reactions.operation('post_story_react')
def post_react():
    # ..do the work..
    return 0

#################################################################################

# create a first admin user
    #with app.app_context():
    #    q = db.session.query(User).filter(User.email == 'example@example.com')
    #    user = q.first()
    #    if user is None:
    #        example = User()
    #        example.username = 'Admin'
    #        example.firstname = 'Admin'
    #        example.lastname = 'Admin'
    #        example.email = 'example@example.com'
    #        example.dateofbirth = dt.datetime(2020, 10, 5)
    #        example.is_admin = True
    #        example.set_password('admin')
    #        db.session.add(example)
    #        db.session.commit()
