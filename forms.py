# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

    
class AddDataForm(FlaskForm):
    table_type = SelectField('Table Type', choices=[('shelter', 'Shelter'), ('food_bank', 'Food Bank'), ('mental_health', 'Mental Health')])
    name = StringField('Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    specialization = StringField('Specialization')
    submit = SubmitField('Add')