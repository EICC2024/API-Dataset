from pathlib import Path

from flask import Flask, request
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import base64


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    profile_photo_path = db.Column(db.String(100), nullable=False)


app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")

db.init_app(app)

with app.app_context():
    db.create_all()


def encode(obj):
    return base64.b64encode(str(obj).encode("utf-8")).decode("utf-8")


@app.post("/signup")
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    photo_path = request.json.get("photo-path")

    user = User.query.filter_by(username=username).first()

    if not user:
        user = User(username=username, password=generate_password_hash(password), profile_photo_path=photo_path)
        
        db.session.add(user)
        db.session.commit()

        return {"message": "User successfully created.!"}
    else:
        return {"error": "User already exists.!"}


@app.get("/user/<int:user_id>")
def user(user_id):
    user = User.query.get(user_id)

    if user:
        try:
            with open(user.profile_photo_path) as file:
                print(user.profile_photo_path)
                profile_photo = encode("".join(file.readlines()))

            return {
                "id": user.id,
                "username": user.username,
                "photo": profile_photo
            }
        except:
            return {"error": "An error occured.!"}
    else:
        return {"error": "User couldn't found.!"}
