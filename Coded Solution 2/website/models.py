#Database is here
#from __init__.py import the database
from . import db
#Helps users login
from flask_login import UserMixin
from sqlalchemy import PickleType

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    dictionaries = db.relationship('Timetable')

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(PickleType, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

