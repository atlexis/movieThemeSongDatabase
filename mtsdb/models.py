from flask_sqlalchemy import SQLAlchemy
from . import db

# Author: Alexander Libot

# This module is used for creating the database structure
# and as classes to create new objects to add to the database.
# OBS! When creating a new database, the current data won't be 
# preserved, so use with caution.

# To create a new database first delete the old one: api/database.db
# Modify this file to contain the structure of the new database.
# Open up a python shell in the project folder and type:
# >>> from api.models import Movie, Theme
# >>> from api import db, create_app
# >>> db.create_all(app=create_app())


# Structure of the database entity containing the movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    imdb = db.Column(db.String(9), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

# Structure of the database entity containing the themes
class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    spotify = db.Column(db.String(22), nullable=False)
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    composer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
