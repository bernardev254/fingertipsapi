from flask import Flask
import os
from backend.auth import auth
from backend.bookmarks import bookmarks
from backend.database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    if test_config is None:
        app.config.from_mapping(
                SECRET_KEY=os.environ.get("SECRET_KEY"),
                SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
                JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                JWT_ACCESS_TOKEN_EXPIRES=False,
                SQLALCHEMY_ECHO=True
                )
    else:
        app.config.from_mapping(test_config)
        
    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app
