from flask import jsonify
from flask_login import UserMixin
from . import create_app
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    clinical_data = db.relationship('ClinicalData', backref='client', lazy=True)

class ClinicalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'test_name': self.test_name,
            'result': self.result,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None
        }

def get_client_data(client_id):
    client = Client.query.get_or_404(client_id)
    data = {
        'client_id': client.id,
        'client_name': client.name,
        'client_email': client.email,
        'clinical_data': [clinical_data.to_dict() for clinical_data in client.clinical_data]
    }
    return jsonify(data)