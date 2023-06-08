from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import configure_views

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'manny manny'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-connection-uri'


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    configure_views(app)

    return app
