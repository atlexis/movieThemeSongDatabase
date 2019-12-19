from flask_sqlalchemy import SQLAlchemy
from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    composer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
