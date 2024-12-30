
import os
from flask import Flask
# def create_app():
app = Flask(__name__,
        template_folder="../templates",
        static_folder="../static",
)

from DropConnect import routes


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


from DropConnect.extensions import sql_db

from DropConnect.routes.home_route import home_bp
from DropConnect.routes.auth_route import auth_bp
from DropConnect.routes.option_route import options_bp


with app.app_context():
    sql_db.create_all()

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(options_bp)



