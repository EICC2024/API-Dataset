from pathlib import Path
from datetime import datetime, timedelta
import base64
import json
from dataclasses import dataclass

from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)

DATE_FORMAT = "%Y/%m/%d-%H:%M:%S"

@dataclass
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username: str = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
db.init_app(app)

with app.app_context():
    db.create_all()


def encode(obj):
    return base64.b64encode(str(obj).encode("utf-8")).decode("utf-8")


def decode(str_value):
    decoded_str = base64.b64decode(str_value.encode("utf-8")).decode("utf-8")
    
    return json.loads(decoded_str.replace("'", '"'))


@app.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = {"username": user.username, "first_request": datetime.now().strftime(DATE_FORMAT), "number_of_request": 1}
        return {"message": "Successfully logged in.!",
                "token": encode(token)}

    return {"error": "Invalid username or password.!"}


@app.get("/users")
def get_users():
    token = request.json.get("token")

    if token:
        try:
            decoded_token = decode(token)

            number_of_request = decoded_token.get("number_of_request")
            first_request = decoded_token.get("first_request")

            if datetime.now() - datetime.strptime(first_request, DATE_FORMAT) < timedelta(seconds=60):
                if number_of_request > 5:
                    return {"error": "Too many requests have been sent.!"}, 429
                else:
                    number_of_request += 1
                    decoded_token["number_of_request"] = number_of_request
            else:
                decoded_token["first_request"] = datetime.now().strftime(DATE_FORMAT)
                decoded_token["number_of_request"] = 1

            return {"token": encode(decoded_token), "users": User.query.all()}
        
        except:
            return {"error": "Unexpected error.!"}
    else:
        return {"error": "Token must be supplied.!"}
    