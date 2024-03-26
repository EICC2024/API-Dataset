from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# List of users (username, privilege, password)
users = [
    {"username": "user1", "privilege": "admin", "password": "password123"},
    {"username": "user2", "privilege": "user", "password": "qwerty456"},
    {"username": "user3", "privilege": "user", "password": "abc123"},
]

@app.route('/')
def index():
    return "Welcome to the User Management System!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = next((user for user in users if user["username"] == username and user["password"] == password), None)
        
        if user:
            if user["privilege"] == "admin":
                return redirect(url_for('admin_home'))
            elif user["privilege"] == "user":
                return redirect(url_for('user_home'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')

@app.route('/login/admin')
def admin_home():
    return render_template('admin_dashboard.html')

@app.route('/login/user')
def user_home():
    return "Welcome to the User Dashboard!"

@app.route('/login/admin/users')
def list_users():
    return render_template('user_list.html', users=users)

if __name__ == '__main__':
    app.run()
