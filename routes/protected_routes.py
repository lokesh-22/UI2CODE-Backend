from flask import Blueprint, jsonify
from utils.auth import token_required
from flask import Blueprint, request, jsonify
from models import db, Car, Review, User
from sqlalchemy.exc import SQLAlchemyError




protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'email': current_user.email,
        'message': 'This is a protected route'
    })


@protected_bp.route('/reviews', methods=['POST'])
@token_required
def post_review(current_user):
    data = request.json
    try:
        review = Review(
            car_id=data['car_id'],
            user_id=current_user.id,
            rating=data['rating'],
            comment=data.get('comment')
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review submitted successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
