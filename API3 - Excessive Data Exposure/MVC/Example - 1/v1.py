from flask import Flask, jsonify

app = Flask(__name__)

# List to store person information (name, surname, balance)
person_list = [
    {"name": "John", "surname": "Doe", "balance": 1000},
    {"name": "Jane", "surname": "Smith", "balance": 1500},
    {"name": "Alice", "surname": "Johnson", "balance": 2000},
]

@app.route('/')
def index():
    return "Welcome to the Home Page"

@app.route('/users', methods=['GET'])
def get_users():
    users = [{"name": person["name"], "surname": person["surname"], "balance": person["balance"]} for person in person_list]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=False)
