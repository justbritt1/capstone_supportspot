
# Imports
from flask import Flask, render_template, request, redirect, url_for, flash 

from models import db, Shelter, FoodBank, MentalHealthFacility

app = Flask(__name__)

# MySQL workbench credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password1993@localhost/resourcelocator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


        
@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    db.create_all()

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