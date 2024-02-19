
# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, render_template


app = Flask(__name__)

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
    # Retrieve shelter names (replace with real data retrieval logic)
    shelter_names = ["Shelter A", "Shelter B", "Shelter C"]  # Example data

    return render_template('shelters.html', shelter_names=shelter_names)

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