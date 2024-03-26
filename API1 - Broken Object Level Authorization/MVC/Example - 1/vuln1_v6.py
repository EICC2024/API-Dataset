from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# List of user data
users = [
    {"id": 1, "username": "john.doe", "name": "John", "surname": "Doe", "balance": 1000, "password": "john123"},
    {"id": 2, "username": "jane.smith", "name": "Jane", "surname": "Smith", "balance": 1500, "password": "jane456"},
    {"id": 3, "username": "alice.johnson", "name": "Alice", "surname": "Johnson", "balance": 2000, "password": "alice789"}
]

# Flag to track successful login
successful_login = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users')
def list_users():
    users_data = '<br>'.join([f"ID: {user['id']}, Username: {user['username']}, Name: {user['name']}, Surname: {user['surname']}, Balance: {user['balance']}" for user in users])
    return users_data

@app.route('/get_user', methods=['GET', 'POST'])
def get_user():
    global successful_login  # Use the global flag

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)
        if user and user['password'] == password:
            successful_login = True
            return redirect(url_for('user_profile', user_id=user['id']))
        return jsonify({'error': 'Authentication failed'})

    return render_template('login.html')

@app.route('/get_user/<int:user_id>')
def user_profile(user_id):
    if successful_login:
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            return jsonify({key: value for key, value in user.items() if key != 'password'})
    return jsonify({'error': 'Access denied'})

if __name__ == '__main__':
    app.run()
