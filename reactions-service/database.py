import datetime as dt
import json
from random import randint

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property

from werkzeug.security import check_password_hash, generate_password_hash

DATABASE_NAME = 'sqlite:///reactions.db'

db = SQLAlchemy()

class Reaction(db.Model):
    __tablename__ = 'reaction'
    reactor_id = db.Column(db.Integer, primary_key=True)

    story_id = db.Column(db.Integer, primary_key=True)
    
    reaction_val = db.Column(db.Integer)

    # Asynchronously updated when the story service confirms
    # that the story 'storyid' exixsts
    marked = db.Column(db.Boolean, default=False)