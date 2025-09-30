from .user import *
from .auth import *
from .initialize import *

from flask import Flask
from app.extensions import db
from app.routes import register_routes 

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    # Register routes
    register_routes(app)

    return app
