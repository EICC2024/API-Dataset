import random
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# List of user data
users = [
    {"id": 1, "username": "john.doe", "name": "John", "surname": "Doe", "email": "john@example.com", "balance": 1000, "password": "john123"},
    {"id": 2, "username": "jane.smith", "name": "Jane", "surname": "Smith", "email": "jane@example.com", "balance": 1500, "password": "jane456"},
    {"id": 3, "username": "alice.johnson", "name": "Alice", "surname": "Johnson", "email": "alice@example.com", "balance": 2000, "password": "alice789"}
]

# Dictionary to store OTPs for password reset
password_reset_otp = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users')
def list_users():
    users_data = '<br>'.join([f"ID: {user['id']}, Username: {user['username']}, Name: {user['name']}, Surname: {user['surname']}, Email: {user['email']}, Balance: {user['balance']}" for user in users])
    return users_data

@app.route('/get_user', methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)
        if user and user['password'] == password:
            return redirect(url_for('user_profile', user_id=user['id']))
        return jsonify({'error': 'Authentication failed'})

    return render_template('login.html')

@app.route('/get_user/<int:user_id>')
def user_profile(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify({key: value for key, value in user.items() if key != 'password'})
    return jsonify({'error': 'User not found'})

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    global password_reset_otp

    if request.method == 'POST':
        email = request.form['email']
        user = next((user for user in users if user['email'] == email), None)
        
        if user:
            # Generate a 3-digit OTP and store it in the dictionary
            generated_otp = f"{random.randint(100, 999)}"
            print(generated_otp)
            password_reset_otp[email] = generated_otp
            
            # Redirect to the OTP input page
            return redirect(url_for('otp_input', email=email))
        else:
            return "Email not found"

    return render_template('forgot_password_email.html')

@app.route('/forgot_password/<email>', methods=['GET', 'POST'])
def otp_input(email):
    global password_reset_otp
    
    if email in password_reset_otp:
        if request.method == 'POST':
            entered_otp = request.form['otp']
            generated_otp = password_reset_otp[email]
            
            if entered_otp == generated_otp:
                user = next((user for user in users if user['email'] == email), None)
                if user:
                    return f"Your password: {user['password']}"
            else:
                return "Invalid OTP"
        
        return render_template('forgot_password_otp.html', email=email)
    else:
        return "OTP not generated"

if __name__ == '__main__':
    app.run()
