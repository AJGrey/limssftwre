"""
This module serves as the entry point for the website.
It initializes the Flask application, sets up the database,
and registers the blueprints for different components of the
website. The `create_app` function creates and configures the
Flask application instance, sets up the database connection
and registers the necessary blueprints. The `db` object is an
instance of SQLAlchemy, which provides an interface to interact
with the database. The `views` and `auth` blueprints define the 
routes and views for the main functionality and authentication
of the website. To start the website, run the `create_app`
function to get the Flask application instance and then run it 
using the `run()` method.

"""

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """Creating the app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'manny manny'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Client, ClinicalData

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
