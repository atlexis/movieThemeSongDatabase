import os

from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

# Author: Alexander Libot
# This module is called when the app is started.
# It sets up the basics of the Flask app.

#db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # Create instance of class
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mtsdb.sqlite'),
    )

    #app.secret_key = b'_5#y2L"F4Q8z\xec]/' # Used for message flashing

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Configure database

    #db.init_app(app)

    #from .route import main
    #app.register_blueprint(main)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import web
    app.register_blueprint(web.bp)
    app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)

    return app
