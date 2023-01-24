from crypt import methods
from email import message
import requests
from bs4 import BeautifulSoup as soup
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS
from backend.database import Bookmark, db

bookmarks = Blueprint("bookmarks", __name__, url_prefix='/api/v1/bookmarks')
CORS(bookmarks, supports_credentials=True)


def getFavicon(domain):
    """ a function that returns a domains favicon url"""
    if 'http' not in domain:
        domain = 'http://' + domain
    page = requests.get(domain)
    mysoup = soup(page.text, features="lxml")
    icon_link = mysoup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = mysoup.find("link", rel="icon")
    if icon_link is None:
        return domain + '/favicon.ico'
    return icon_link["href"]

def getTittle(domain):
    ''' returns domains title'''
    if 'http' not in domain:
        domain = 'http://' + domain
    page = requests.get(domain)
    mysoup = soup(page.text)
    title = mysoup.title.get_text()
    return title


@cross_origin(origins='*',methods=['POST','OPTIONS'])
@bookmarks.route('/new', methods=['POST','OPTIONS'])
@jwt_required()
def add_bookmark():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    data = request.get_json()
    title = data.get('title')
    url = data.get('url')
    body = data.get('body')
    icon = data.get('icon')
    category = data.get('category')
    user_id = get_jwt_identity()
    try:
        bookmark = Bookmark(title=title,url=url,body=body,icon=icon,category=category,user_id=user_id)
        if bookmark:
            db.session.add(bookmark)
            db.session.commit()
            return jsonify({
            "message": "bookmark created"
        }), 201
    except Exception:
        return jsonify({
            "error":"error saving bookmark"
        }), 500
    else:
        return jsonify({
            "error":"error saving bookmark"
        }), 500

@cross_origin(origins='*',methods=['POST','OPTIONS'])
@bookmarks.route('/getBookmarkDetails', methods=['POST','OPTIONS'])
@jwt_required()
def get_bookmark_details():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    data = request.get_json()
    url = data.get("url")
    try:
        icon = getFavicon(url)
        title = getTittle(url)
        return jsonify({
            "icon": icon,
            "title": title
        }), 200
    except Exception:
        return jsonify({"error":"invalid url"}), 404
    

@cross_origin(methods=['DELETE','OPTIONS'])
@bookmarks.route('/remove', methods=['DELETE',])
@jwt_required()
def remove_bookmark():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    data = request.get_json()
    id = data.get("id")
    try:
        bookmark = Bookmark.query.filter_by(id=id).first()
        if bookmark:
            db.session.delete(bookmark)
            db.session.commit()
            return jsonify({
                "mesage":"bookmark deleted"
            }), 200
        return jsonify({
            "error":"error deleting bookmark"
        }), 500
    except Exception:
        return jsonify({
            "error": "error deleting bookmark"
        }), 500

@cross_origin(methods=['GET','OPTIONS'])
@bookmarks.route('/my_bookmarks')
@jwt_required()
def get_bookmarks():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    user_id = get_jwt_identity()
    bookmarksList = []
    try:
        bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
        if bookmarks:
            for book in bookmarks:
                my_obj = {
                    "title":book.title,
                    "id": book.id,
                    "body":book.body,
                    "url":book.url,
                    "icon":book.icon
                }
                bookmarksList.append(my_obj)
            return jsonify({
                "bookmarks":bookmarksList
            }), 200
        return jsonify({
            "bookmarks": bookmarksList
        }), 200
    except Exception:
        return jsonify({
            "error":"failed to fetch bookmarks"
        }), 500

@cross_origin(methods=['PATCH','OPTIONS'])
@bookmarks.route('/update',methods=['PATCH'])
@jwt_required()
def my_update():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    data = request.get_json()
    id = data.get('id')
    try:
        book = Bookmark.query.filter_by(id=id).first()
        if book:
            for key, value in data:
                if key:
                    book.key = value
            db.session.commit()
            return jsonify({"message":"updated successfully"}), 200
        return jsonify({"msg":"update Error"}), 500
    except:
        return jsonify({"msg":"update Error"}), 500




