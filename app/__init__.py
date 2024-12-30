
import os
from flask import Flask
# def create_app():
app = Flask(__name__,
        template_folder="../templates",
        static_folder="../static",
)

from app import routes


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY




