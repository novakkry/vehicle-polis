from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from marketplace.config import Config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'This page is accessible only to logged in users. Please log in.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    # for heroku uncomment the next line and comment database config in config.py
    # app.config.from_mapping(SQLALCHEMY_DATABASE_URI = os.environ['HEROKU_POSTGRESQL_COBALT_URL']) #maybe should be DATABASE_URL

    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        from marketplace import routes

    return app