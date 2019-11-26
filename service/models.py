import json

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property

from service.extensions import db


class Reaction(db.Model):
    __tablename__ = 'reaction'
    reactor_id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(db.Integer, primary_key=True)
    
    reaction_val = db.Column(db.Integer)

    # marked should be no longer needed, as we update immediately
    # and send an asynchronous update to the story service
    # marked = db.Column(db.Boolean, default=False)
