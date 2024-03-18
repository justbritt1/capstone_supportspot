from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    table_type = db.Column(db.Enum('shelter', 'food_bank', 'mental_health'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    specialization = db.Column(db.String(255))

    def __repr__(self):
        return f"<Resource(id={self.id}, name={self.name}, table_type={self.table_type})>"