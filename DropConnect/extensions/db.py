import os
from flask_sqlalchemy import SQLAlchemy
from DropConnect import app
from dotenv import load_dotenv

load_dotenv()

# SQLite configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']="7894556123"

sql_db = SQLAlchemy(app)