from flask import Blueprint, render_template, url_for

views = Blueprint('views', __name__, static_folder='static')

@views.route('/')
def home():
    return render_template('index.html')

def configure_views(app):
    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        # Handle cleint GET reguest
        return 'Client ID: {}'.format(client_id)