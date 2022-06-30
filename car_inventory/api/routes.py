from flask import Blueprint, jsonify, request
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema 

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}

# Create Car Endpoint
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    make = request.json['make']
    model = request.json['model']
    vehicle_type = request.json['vehicle_type']
    year = request.json['year']
    color = request.json['color']
    drive = request.json['drive']
    price = request.json['price']
    top_speed = request.json['top_speed']
    weight = request.json['weight']
    seats = request.json['seats']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    car = Car(name, description, make, model, vehicle_type, year, color, drive, price, top_speed, weight, seats, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


# Retrieve all Car Endpoints
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# Retrieve a single Car Endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = cars_schema.dump(car)  # why isn' this car showing up?
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401


# Update Car
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.name = request.json['name']
    car.description = request.json['description']
    car.make = request.json['make']
    car.model = request.json['model']
    car.vehicle_type = request.json['vehicle_type']
    car.year = request.json['year']
    car.color = request.json['color']
    car.drive = request.json['drive']
    car.price = request.json['price']
    car.top_speed = request.json['top_speed']
    car.weight = request.json['weight']
    car.seats = request.json['seats']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete Car
@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

