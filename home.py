from flask import Blueprint

home = Blueprint("home", __name__)

@home.get('/')
def welcome():
    return {'message': 'Welcome to bookmarks'}
