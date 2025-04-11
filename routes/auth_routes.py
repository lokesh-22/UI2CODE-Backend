from flask import Blueprint, request, jsonify, current_app
from models import db, User
import bcrypt
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')
    password = data.get('password')
    gender = data.get('gender')

    if not all([name, email, address, phone, password, gender]):
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, email=email, address=address, phone=phone, password=hashed_pw, gender=gender)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, current_app.config['SECRET_KEY'], algorithm="HS256")

            if isinstance(token, bytes):
                token = token.decode('utf-8')

            return jsonify({'token': token}), 200

        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
