from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"User {self.username}"
    
    # Flask-Login required methods and attributes
    def is_active(self):
        """Return True if the user account is active."""
        return True  # or implement logic to check if user account is active

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True  # or implement logic to check if user is authenticated

    def is_anonymous(self):
        """Return False, because a registered user is never anonymous."""
        return False

    def get_id(self):
        """Return the user's unique id (e.g., primary key)."""
        return str(self.id)

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    table_type = db.Column(db.Enum('shelter', 'food_bank', 'mental_health'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    specialization = db.Column(db.String(255))
    latitude = db.Column(db.Float)  # New column for latitude
    longitude = db.Column(db.Float)  # New column for longitude

    def __repr__(self):
        return f"<Resource(id={self.id}, name={self.name}, table_type={self.table_type})>"