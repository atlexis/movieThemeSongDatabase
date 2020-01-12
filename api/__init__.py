from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Author: Alexander Libot
# This module is called when the app is started.
# It sets up the basics of the Flask app.

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) # Create instance of class
    app.secret_key = b'_5#y2L"F4Q8z\xec]/' # Used for message flashing

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Configure database

    db.init_app(app)

    from .route import main
    app.register_blueprint(main)

    return app
