from pathlib import Path

from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import requests

from config import SECRET_KEY, LOGIN_SERVICE

app = Flask(__name__)
path = Path(__file__)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.post("/api/login")
def login():
    login_type = request.args.get("type")
    response = {"error": "Couldn't be logged in.!"}

    if login_type == "username":
        response = username_login(**request.json)
    else:
        response = login_service(**request.json)

    return response


def username_login(**params):
    try:
        username = params.get("username")
        password = params.get("password")

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            token = jwt.encode({"username": user.username}, app.secret_key, algorithm="HS256")

            return {"message": "Successfully logged in.!", "token": token}
        else:
            return {"error": "Invalid username or password.!"}
    except:
        return {"error": "Unsucessful login.!"}


def login_service(**params):
    response = requests.post(LOGIN_SERVICE + "/api/login", data=params, json=True)

    if response.json().get("success"):
        token = jwt.encode({"username": response.json().get("username")}, app.secret_key, algorithm="HS256")

        return {"message": "Successfully logged in.!", "token": token}
    else:
        return {"error": "Invalid username or password.!"}
