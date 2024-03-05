
# Imports
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import ShelterForm, FoodBankForm, MentalHealthForm
from models import db, Shelter, FoodBank, MentalHealthFacility

app = Flask(__name__)

# MySQL workbench credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password1993@localhost/resourcelocator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1993'  

# Initialize the database with app
db.init_app(app)
migrate = Migrate(app, db)
        
@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    # Initialize the database with the app context
    with app.app_context():
        db.create_all()

# Route for the admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    shelter_form = ShelterForm()
    food_bank_form = FoodBankForm()
    mental_health_form = MentalHealthForm()

    if request.method == 'POST':
        if shelter_form.validate_on_submit():
            shelter = Shelter(
                name=shelter_form.name.data,
                capacity=shelter_form.capacity.data,
                location=shelter_form.location.data,
                contact_phone=shelter_form.contact_phone.data
            )
            db.session.add(shelter)
            db.session.commit()

        elif food_bank_form.validate_on_submit():
            food_bank = FoodBank(
                name=food_bank_form.name.data,
                capacity=food_bank_form.capacity.data,
                location=food_bank_form.location.data,
                contact_phone=food_bank_form.contact_phone.data
            )
            db.session.add(food_bank)
            db.session.commit()

        elif mental_health_form.validate_on_submit():
            mental_health = MentalHealthFacility(
                name=mental_health_form.name.data,
                specialization=mental_health_form.specialization.data,
                location=mental_health_form.location.data,
                contact_phone=mental_health_form.contact_phone.data
            )
            db.session.add(mental_health)
            db.session.commit()

        
        return redirect(url_for('admin'))

    shelters = Shelter.query.all()
    food_banks = FoodBank.query.all()
    mental_health_facilities = MentalHealthFacility.query.all()

    return render_template('admin.html', shelter_form=shelter_form, food_bank_form=food_bank_form, mental_health_form=mental_health_form, shelters=shelters, food_banks=food_banks, mental_health_facilities=mental_health_facilities)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic here
        # For simplicity, you can just check hardcoded credentials

        # Example: Check if username is 'admin' and password is 'password'
        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))  # Redirect to the dashboard after successful login
        else:
            error = 'Invalid credentials. Please try again.'

        return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Simulate data for the dashboard (replace with real data retrieval logic)
    user_count = len(users)  # Assuming 'users' is a list of registered users

    # Additional data or logic for the dashboard
    # ...

    return render_template('dashboard.html', user_count=user_count)

@app.route('/shelters')
def shelters():
    # Retrieve shelter names from the database
    shelter_names = Shelter.query.with_entities(Shelter.name).all()

    return render_template('shelters.html', shelter_names=shelter_names)

@app.route('/food_banks')
def food_banks():
    # Retrieve food bank names from the database
    food_banks = FoodBank.query.all()

    return render_template('food_banks.html', food_banks=food_banks)

@app.route('/mental_health')
def mental_health():
    # Retrieve mental health facilities (replace with real data retrieval logic)
    mental_health_facilities = MentalHealthFacility.query.all()

    return render_template('mental_health.html', mental_health_facilities=mental_health_facilities)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your registration logic here
        # For simplicity, you can just store the credentials in a list (not secure for production)

        # Example: Store username and password in a list
        users.append({'username': username, 'password': password})

        return redirect(url_for('login'))

    return render_template('register.html')

users = []


if __name__ == '__main__':
    app.run(debug=True)