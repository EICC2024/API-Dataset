from pathlib import Path
from dataclasses import dataclass
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


app = Flask(__name__)
path = Path(__file__)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")

db = SQLAlchemy(app)


@dataclass
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username: str = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.post("/register")
def register():
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        user = User(username=username, password=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        os.system(f"echo 'User with username {username} has been created.' >> {path.parent}/log.txt")

        return {"message": "User successfully created.!"}
    except Exception as e:
        print(e)
        return {"error": "User couldn't be created.!"}

        