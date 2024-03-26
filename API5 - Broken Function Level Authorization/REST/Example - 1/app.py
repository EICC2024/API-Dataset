from pathlib import Path
from datetime import datetime, timedelta
import base64
import json
from dataclasses import dataclass

from flask import Flask, request
from werkzeug.security import check_password_hash, generate_password_hash
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
        token = {"username": user.username}
        return {"message": "Successfully logged in.!",
                "token": encode(token)}

    return {"error": "Invalid username or password.!"}



@app.post("/change-password")
def change_password():
    token = request.json.get("token")
    password = request.json.get("password")

    if token:
        try:
            if token := decode(token):
                user = User.query.filter_by(username=token.get("username")).first()

                if user:
                    user.password = generate_password_hash(password)
                    db.session.commit()

                    return {"message": "Password has been changed.!"}
                else:
                    return {"message": "User couldn't found.!"}
            else:
                raise Exception("Invalid token.!")
        except:
            return {"error": "Error occured.!"}
    else:
        return {"error": "Token must be supplied.!"}