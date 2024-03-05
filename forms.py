# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class ShelterForm(FlaskForm):
    name = StringField('Shelter Name')
    capacity = IntegerField('Capacity')
    location = StringField('Location')
    contact_phone = StringField('Contact Phone')
    submit = SubmitField('Add Shelter')

class FoodBankForm(FlaskForm):
    name = StringField('Food Bank Name')
    capacity = IntegerField('Capacity')
    location = StringField('Location')
    contact_phone = StringField('Contact Phone')
    submit = SubmitField('Add Food Bank')

class MentalHealthForm(FlaskForm):
    name = StringField('Mental Health Facility Name')
    specialization = StringField('Specialization')
    location = StringField('Location')
    contact_phone = StringField('Contact Phone')
    submit = SubmitField('Add Mental Health Facility')