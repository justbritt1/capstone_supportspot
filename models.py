from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Shelter(db.Model):
    shelter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(20))

class FoodBank(db.Model):
    foodbank_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(20))

class MentalHealthFacility(db.Model):
    facility_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(255))
    location = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(20))