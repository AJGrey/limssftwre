from os import path
from flask import Flask, session, g, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .auth import auth

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    """Create and configure the flask application instance"""
    app = Flask(__name__)
    DB_NAME = "database.db"
    app.config['SECRET_KEY'] = 'manny manny'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    db.app = app

    # Importing and registering blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Initialize bcrypt
    bcrypt.init_app(app)

    # Custom user authentication logic
    from .models import User
    
    def create_database(app):
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email.lower()).first()
            if user and bcrypt.check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                session['user_id'] = user.id
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password, try again.', category='error')

        return render_template("login.html")

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('views.home'))

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
