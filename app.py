from flask import Flask
import os
from auth import auth
from bookmarks import bookmarks
from database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app, supports_credentials=True)
app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_ACCESS_TOKEN_EXPIRES=False,
    SQLALCHEMY_ECHO=True
    )
        
db.app = app
db.init_app(app)

JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(bookmarks)

