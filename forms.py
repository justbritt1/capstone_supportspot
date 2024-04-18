# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

    
class AddDataForm(FlaskForm):
    table_type = SelectField('Table Type', choices=[('shelter', 'Shelter'), ('food_bank', 'Food Bank'), ('mental_health', 'Mental Health')])
    name = StringField('Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    specialization = StringField('Specialization')
    submit = SubmitField('Add')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')