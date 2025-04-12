from flask import Blueprint, request, jsonify, current_app
from models import db, User
import bcrypt
import jwt
import datetime
import logging


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

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(name=name, email=email, address=address, phone=phone, password=hashed_pw, gender=gender)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# Set up logging
logging.basicConfig(level=logging.DEBUG)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        logging.debug(f"User found: {user.email}")
        # Ensure both password and hash are bytes
        hashed_password = user.password.encode('utf-8') if isinstance(user.password, str) else user.password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, current_app.config['SECRET_KEY'], algorithm="HS256")

            if isinstance(token, bytes):
                token = token.decode('utf-8')

            return jsonify({'token': token}), 200

    logging.warning("Invalid login attempt")
    return jsonify({'message': 'Invalid credentials'}), 401
