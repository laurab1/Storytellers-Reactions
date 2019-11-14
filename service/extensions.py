# -*- coding: utf-8 -*-

from celery import Celery
celery = Celery()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
