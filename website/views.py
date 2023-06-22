from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from flask import flash
from .models import Client, ClinicalData
from . import db
import sqlite3

views = Blueprint('views', __name__, static_folder='static')


@views.route('/')
def home():
    """Returns home page"""
    return render_template('index.html')


@views.route('/submit_enquiry', methods=['POST'])
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

    return "Enquiry submitted successfully!"  # You can customize the response message


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@views.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    """Adding new client to the database"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        # Create a new instance of the Client model
        new_client = Client(name=name, email=email, phone=phone, address=address)

        # Add the new client to the database
        db.session.add(new_client)
        db.session.commit()

        # Redirect to client details page
        return redirect(url_for('views.client_details', client_id=new_client.id))

    return render_template('add_client.html')


@views.route('/clients/<int:client_id>', methods=['GET'])
def client_details(client_id):
    """Retrieve details of a client"""
    client = Client.query.get_or_404(client_id)
    return render_template('client_details.html', client=client)


@views.route('/clients/<int:client_id>/clinical_data', methods=['GET', 'POST'])
def create_clinical_data(client_id):
    """Create clinical data for a client"""
    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        test_name = request.form.get('test_name')
        result = request.form.get('result')

        clinical_data = ClinicalData(test_name=test_name, result=result, client=client)
        db.session.add(clinical_data)
        db.session.commit()

        # Redirect to client details page
        return redirect(url_for('views.client_details', client_id=client_id))

    return render_template('create_clinical_data.html', client=client)


# Register the blueprint with the Flask application
def configure_views(app):
    app.register_blueprint(views)


# Call the configure_views function in your create_app function
def create_app():
    app = Flask(__name__)
    # ... app configuration and other setup ...

    # Register views blueprint
    configure_views(app)

    return app
