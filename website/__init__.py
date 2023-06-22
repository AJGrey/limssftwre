from os import path
from flask import Flask, session, g, request, render_template, redirect, url_for, flash
from flask import flash
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
            with app.app_context():
                db.create_all()


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()
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
        db.session.delete(g.user)
        db.session.commit()
        return redirect(url_for('views.home'))
    
    @app.route('/submit_enquiry', methods=['POST'])
    def submit_enquiry():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Create a table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS enquiries
                 (name TEXT, email TEXT, message TEXT)''')

        # Insert the enquiry data into the table
        c.execute("INSERT INTO enquiries VALUES (?, ?, ?)", (name, email, message))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        flash('Message Submitted', 'success')
        return jsonify({'redirect': '/'})

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

    create_database(app)

    return app
   