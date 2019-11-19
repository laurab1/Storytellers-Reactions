import json

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property



db = SQLAlchemy()

class Reaction(db.Model):
    __tablename__ = 'reaction'
    reactor_id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(db.Integer, primary_key=True)
    
    reaction_val = db.Column(db.Integer)

    # Asynchronously updated when the story service confirms
    # that the story 'storyid' exixsts
    marked = db.Column(db.Boolean, default=False)
