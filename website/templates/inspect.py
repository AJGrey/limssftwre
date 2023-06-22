from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define your models here

# Create an inspector object
inspector = inspect(db.engine)

# Get a list of all table names
table_names = inspector.get_table_names()

# Print the table names
for table_name in table_names:
    print(table_name)
