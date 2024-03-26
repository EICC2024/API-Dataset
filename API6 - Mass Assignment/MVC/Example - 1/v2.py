from flask import Flask, render_template, request

app = Flask(__name__)

# Sample user data
user_list = [
    {"username": "user123", "email": "user123@example.com", "balance": 1000},
    {"username": "john_doe", "email": "john.doe@example.com", "balance": 500},
    {"username": "jane_smith", "email": "jane.smith@example.com", "balance": 750}
]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['POST', 'PUT'])
def signup():
    data = request.get_json()
    if data:
        username = data.get('username')
        email = data.get('email')
        balance = data.get('balance', 0)
        user_list.append({"username": username, "email": email, "balance": balance})
        return {"message": "User added successfully"}, 201
    return {"message": "Invalid data"}, 400

@app.route('/users')
def users():
    return render_template('users.html', user_list=user_list)

if __name__ == '__main__':
    app.run()
