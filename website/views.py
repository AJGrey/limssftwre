from flask import Blueprint, render_template, url_for

views = Blueprint('views', __name__, static_folder='static')

@views.route('/')
def home():
    return render_template('index.html')
