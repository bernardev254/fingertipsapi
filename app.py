from flask import Flask
import os
from home import home
from auth import auth
from bookmarks import bookmarks
from database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config_by_name
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, instance_relative_config=True)
CORS(app, supports_credentials=True)
app.config.from_object(config_by_name["prod"])
with app.app_context():
    db.app = app
    db.init_app(app)
    #db.create_all()

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(home)
if __name__ == "__main__":
    app.run()
