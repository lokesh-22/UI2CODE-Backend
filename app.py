from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt
import datetime
from functools import wraps
from models import db, User


from dotenv import load_dotenv
load_dotenv()

import os


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_dev_secret')

db.init_app(app)

@app.before_request
def create_tables_once():
    if not hasattr(app, 'db_initialized'):
        db.create_all()  # or db.drop_all(); db.create_all()
        app.db_initialized = True


# 🔒 Decorator for protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                bearer = request.headers['Authorization']
                token = bearer.split()[1]  # Remove "Bearer "
            except:
                return jsonify({'message': 'Token is missing or invalid'}), 403

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(current_user, *args, **kwargs)
    return decorated
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')
    password = data.get('password')

    if not all([name, email, address, phone, password]):
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, email=email, address=address, phone=phone, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token.decode('utf-8')}), 200


    return jsonify({'message': 'Invalid credentials'}), 401

# 🎯 Protected route example
@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'email': current_user.email,
        'message': 'This is a protected route'
    })

if __name__ == '__main__':
    app.run(debug=True)
