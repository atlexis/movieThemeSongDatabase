from flask_sqlalchemy import SQLAlchemy
from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    composer = db.Column(db.String(200), nullable=False)
    imdb = db.Column(db.String(9), nullable=False)
#    themes = db.relationship('Theme', backref='movie', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.id

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    spotify = db.Column(db.String(22), nullable=False)
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
