from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Sample user data (username: (password, blocked, unsuccessful_attempts))
user_data = {
    'user1': ('password1', False, 0),
    'user2': ('password2', False, 0),
    'user3': ('password3', False, 0)
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/v1/login', methods=['GET', 'POST'])
def v1_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in user_data:
            stored_password, _, _ = user_data[username]
            
            if password == stored_password:
                return f'Welcome, {username}!'
            else:
                return 'Invalid password. Please try again.'
        else:
            return 'User not found.'
    
    return render_template('v1_login.html')

@app.route('/v2/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in user_data:
            stored_password, blocked, unsuccessful_attempts = user_data[username]
            
            if blocked:
                return 'Your account is blocked.'
            
            if password == stored_password:
                if unsuccessful_attempts >= 3:
                    user_data[username] = (stored_password, True, unsuccessful_attempts)
                    return 'Your account is now blocked due to too many unsuccessful attempts.'
                user_data[username] = (stored_password, blocked, 0)  # Reset unsuccessful attempts
                return f'Welcome, {username}!'
            else:
                user_data[username] = (stored_password, blocked, unsuccessful_attempts + 1)
                if unsuccessful_attempts >= 3:
                    user_data[username] = (stored_password, True, unsuccessful_attempts)
                    return 'Your account is now blocked due to too many unsuccessful attempts.'
                return 'Invalid credentials. Please try again.'
        else:
            return 'User not found.'
    
    return render_template('login.html')

@app.route('/users')
def display_users():
    return render_template('users.html', users=user_data)

if __name__ == '__main__':
    app.run(debug=False)
