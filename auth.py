from crypt import methods
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import User, db
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin, CORS
import requests
import html
from bs4 import BeautifulSoup as soup


auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')
CORS(auth, supports_credentials=True)


@auth.route('/register',methods=['POST','OPTIONS',])
@cross_origin(origins='*',methods=['POST','OPTIONS',])
def register():
    if request.method == 'OPTIONS':
        return jsonify({"msg":"success"}), 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if len(password) < 6:
        return jsonify({
            'error': 'password too short'
            }), 400
    if len(username) <3:
        return jsonify({
            'error': 'username too short'
            }), 400
    if " " in username:
        return jsonify({
            'error': 'username should have no spaces'
            }), 400
    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'email already exixts'
            }), 400
    if User.query.filter_by(username=username).first():
        return jsonify({
            'error': 'username already exists'
            }), 400
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username,email=email,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message':"user created",
            'username': username,
            'email': email
            }), 201

@auth.route('/login',methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = User.query.filter_by(email=email).first()
        if user:
            correct_passwd = check_password_hash(user.password, password)

            if correct_passwd:
                access = create_access_token(identity=user.id)
               
                return jsonify({
                    'access':access,
                    'username':user.username,
                   'email':user.email}), 200
                       
            return jsonify({
                'error': 'wrong credentials'
                }), 401
        return jsonify({
            "msg": "Not Found"
            }), 404     
    except Exception:
        return jsonify({
            "msg": "Not Found"
        }), 404



@auth.route("/proxy",methods=["POST","OPTIONS"])
@cross_origin(origins='*',methods=['POST','OPTIONS',])
def proxy():
    data = request.get_json()
    url = data.get('url')
    response = requests.get(url)
    page = soup(response.text, "html.parser").prettify().replace('\n', " ")
    return jsonify(page), 200
    
    
@app.route("/render_page", methods=["POST", "OPTIONS"])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'])
def proxy():
    data = request.get_json()
    url = data.get('url')
    response = requests.get(url)
    page = response.text

    # Perform preprocessing and rendering
    # For example, let's prettify the HTML using BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    prettified_html = soup.prettify()

    # Replace any newline characters with spaces
    prettified_html = prettified_html.replace('\n', ' ')

    # Get the URLs of any additional assets (e.g., CSS, JS, images) from the parsed HTML
    css_urls = []
    js_urls = []
    image_urls = []

    # Extract the URLs of CSS files
    css_tags = soup.find_all('link', {'rel': 'stylesheet'})
    for css_tag in css_tags:
        css_urls.append(css_tag['href'])

    # Extract the URLs of JavaScript files
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if script_tag.get('src'):
            js_urls.append(script_tag['src'])

    # Extract the URLs of image files
    image_tags = soup.find_all('img')
    for image_tag in image_tags:
        if image_tag.get('src'):
            image_urls.append(image_tag['src'])

    # Create a dictionary containing the prettified HTML and asset URLs
    bookmark_data = {
        'html': prettified_html,
        'css': css_urls,
        'js': js_urls,
        'images': image_urls
    }

    return jsonify(bookmark_data), 200    
