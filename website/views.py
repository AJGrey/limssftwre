from flask import Blueprint, render_template, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Client, ClinicalData
from . import db
import json

views = Blueprint('views', __name__, static_folder='static')

@views.route('/')
def home():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@views.route('/add_client', methods=['GET','POST'])
@login_required
def add_client():
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

        return redirect(url_for('views.client_details', client_id=client.id))  # Redirect to home page after successful submission

    return render_template('add_client.html')  # Display the form

def configure_views(app):
    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        # Handle cleint GET reguest
        return 'Client ID: {}'.format(client_id)

@views.route('/clients/<int:client_id>', methods=['GET'])
def client_details(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_details.html', client=client)

@views.route('/clients/<int:client_id>/clinical_data', methods=['GET', 'POST'])
def create_clinical_data(client_id):
    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        test_name = request.form.get('test_name')
        result = request.form.get('result')

        clinical_data = ClinicalData(test_name=test_name, result=result, client=client)
        db.session.add(clinical_data)
        db.session.commit()

        return redirect(url_for('views.client_details', client_id=client_id))

    return render_template('create_clinical_data.html', client=client)