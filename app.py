
# Imports
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddDataForm
from models import db, Resource

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

@app.route('/dashboard')
def dashboard():
    # Simulate data for the dashboard (replace with real data retrieval logic)
    user_count = len(users)  # Assuming 'users' is a list of registered users

    # Additional data or logic for the dashboard
    # ...

    return render_template('dashboard.html', user_count=user_count)

@app.route('/resources')
def resources():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/delete/<int:data_id>', methods=['POST'])
def delete_data(data_id):
    # Logic to delete the data with the given ID
    resource = Resource.query.get(data_id)
    if resource:
        db.session.delete(resource)
        db.session.commit()
        flash('Resource deleted successfully', 'success')
    else:
        flash('Resource not found', 'error')

    return redirect(url_for('admin'))

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