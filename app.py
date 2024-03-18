'''
Support Spot Web App
By: Brittany and Justin
"2024"
'''

# Imports
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
#from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from forms import AddDataForm
from models import db, Resource, User
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

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

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the ZIP code from the form
        zip_code = request.form['zip_code']
    
        # Geocode the ZIP code
        geolocator = Nominatim(user_agent="resource_locator")
        location = geolocator.geocode(zip_code)
    
        if location:
            user_coordinates = (location.latitude, location.longitude)
            # Query the database to get all resources
            resources = Resource.query.all()
        
            # Calculate distance between user and each resource
            for resource in resources:
                resource_coordinates = (resource.latitude, resource.longitude)
                distance = geodesic(user_coordinates, resource_coordinates).miles
                resource.distance = distance  # Add distance attribute to resource object
        
            # Sort resources by distance
            resources_sorted = sorted(resources, key=lambda x: x.distance)
        
            return render_template('search_results.html', resources=resources_sorted)
        else:
            flash('Invalid ZIP code', 'error')
            return redirect(url_for('resources'))
    else:
        # Render the search form template
        return render_template('search_results.html')

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