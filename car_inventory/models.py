from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Secrets Module (from by Python)
import secrets

# Imports for Flask_Login
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database"


class Car(db.Model): 
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150), nullable = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    vehicle_type = db.Column(db.String(150))
    year = db.Column(db.String(150))
    color = db.Column(db.String(150))
    drive = db.Column(db.String(150))
    price = db.Column(db.Numeric(precision=10, scale=2))
    top_speed = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    seats = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, description, make, model, vehicle_type, year, color, drive, price, top_speed, weight, seats, user_token, id = '' ):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.make = make
        self.model = model
        self.vehicle_type = vehicle_type
        self.year = year
        self.color = color
        self.drive = drive
        self.price = price
        self.top_speed = top_speed
        self.weight = weight
        self.seats = seats
        self.user_token = user_token

    def __repr__(self):
        return f"The following Car has been added: {self.name}"

    def set_id(self):
        return secrets.token_urlsafe()

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'make', 'model', 'vehicle_type', 'year', 'color', 'drive', 'price', 'top_speed', 'weight', 'seats']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)
