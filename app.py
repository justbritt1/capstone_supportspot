'''
Support Spot Web App
By: Brittany and Justin
"2024"
'''

# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
#from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from sqlalchemy import or_
from forms import AddDataForm
from models import db, Resource, User
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut


app = Flask(__name__)

# MySQL workbench credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password1993@localhost/resourcelocator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1993'  

# Configuration for the users database
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'mysql+mysqlconnector://root:password1993@localhost/users'
}


# Initialize the database with app
db.init_app(app)
migrate = Migrate(app, db)

def create_app():
    # Call geocode_and_update() function within the application context
    with app.app_context():
        geocode_and_update()

# Function to geocode address and update database
# Define the function for geocoding and updating the database
def geocode_and_update():
    print("Inside geocode_and_update")
    resources_without_coordinates = Resource.query.filter_by(latitude=None, longitude=None).all()
    geolocator = Nominatim(user_agent="resource_locator")

    # Increase timeout to 10 seconds (adjust as needed)
    timeout = 10  

    for resource in resources_without_coordinates:
        try:
            location = geolocator.geocode(resource.location, timeout=timeout)
            if location:
                print(f"Geocoded location for {resource.name}: {location.latitude}, {location.longitude}")
                resource.latitude = location.latitude
                resource.longitude = location.longitude
        except GeocoderTimedOut:
            print(f"Geocoding request timed out for {resource.name}")
            continue

    db.session.commit()
create_app()

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
    add_data_form = AddDataForm()

    if request.method == 'POST':
        if add_data_form.validate_on_submit():
            table_type = add_data_form.table_type.data
            name = add_data_form.name.data
            capacity = add_data_form.capacity.data
            location = add_data_form.location.data
            contact_phone = add_data_form.contact_phone.data
            specialization = add_data_form.specialization.data

        # Create a new resource entry based on the selected type
            resource = Resource(
                table_type=table_type,
                name=name,
                capacity=capacity,
                location=location,
                contact_phone=contact_phone,
                specialization=specialization
            )
            db.session.add(resource)
            db.session.commit()

            return redirect(url_for('admin'))

    # Fetch all resources to display in the admin page
    resources = Resource.query.all()

    return render_template('admin.html', add_data_form=add_data_form, resources=resources)

    
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

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Resources 
@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        # Handle the form submission for zip code search
        zip_code = request.form.get('zip_code')
        # Perform zip code search logic...
        return redirect(url_for('search'))

    # For GET requests, render the resources page as usual
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

# Map of NC
@app.route('/map')
def map_page():
    return render_template('map.html')

# API route to get a list of all resources
@app.route('/api/resources')
def get_resources():
    # Query the database to retrieve all Resource objects
    resources = Resource.query.all()
    resources_list = []
    # Iterate through each resource object retrieved from the database
    for resource in resources:
        resources_list.append({
            'name': resource.name,
            'address': resource.location,
            'latitude': resource.latitude,
            'longitude': resource.longitude,
            'contact': resource.contact_phone  
        })
    # Return the list of resources as JSON  
    return jsonify(resources_list)

# Delete button for resource data
@app.route('/delete/<int:data_id>', methods=['POST'])
def delete_data(data_id):
    # Check if the referrer is the admin page
    if request.referrer and '/admin' in request.referrer:
        # Logic to delete the data with the given ID
        resource = Resource.query.get(data_id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
            flash('Resource deleted successfully', 'success')
        else:
            flash('Resource not found', 'error')
    else:
        flash('Unauthorized deletion attempt', 'error')

    return redirect(url_for('admin'))

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, email=email, password_hash=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)