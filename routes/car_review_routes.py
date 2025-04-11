from flask import Blueprint, request, jsonify
from models import db, Car, Review, User
from sqlalchemy.exc import SQLAlchemyError

car_routes = Blueprint('car_routes', __name__)

# Create a new car (POST /cars)
@car_routes.route('/cars', methods=['POST']) # Optional, if adding cars requires authentication
def create_car():
    data = request.json
    try:
        car = Car(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            heroimage=data['heroimage'],
            images=data['images'],
            availableColours=data['availableColours']
        )
        db.session.add(car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all cars with minimal info (GET /cars)
@car_routes.route('/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    return jsonify([
        {
            'id': car.id,
            'title': car.title,
            'price': car.price,
            'heroimage': car.heroimage
        } for car in cars
    ])

# Get a car by ID with full details (GET /cars/<int:car_id>)
@car_routes.route('/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify({
        'id': car.id,
        'title': car.title,
        'description': car.description,
        'price': car.price,
        'heroimage': car.heroimage,
        'images': car.images,
        'availableColours': car.availableColours
    })

# Post a review for a car (POST /reviews)

# Get reviews by car ID (GET /reviews/<int:car_id>)
@car_routes.route('/reviews/<int:car_id>', methods=['GET'])
def get_reviews_by_car(car_id):
    reviews = Review.query.filter_by(car_id=car_id).all()
    return jsonify([
        {
            'user': review.user.name,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews
    ])
