from pathlib import Path

from flask import Flask, request
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import requests

from config import SECRET_KEY, EMAIL_SERVICE_URL


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/signup")
def signup():
    email = request.json.get("email")
    password = request.json.get("password")

    if is_email_valid(email):
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(email=email, password=generate_password_hash(password))
            
            db.session.add(user)
            db.session.commit()

            token = jwt.encode({"email": email}, app.secret_key, algorithm="HS256")

            return {"message": "Successfully logged in.!", "token": token}
        else:
            return {"error": "User already exists.!"}
    else:
        return {"error": "Invalid email address.!"}


def is_email_valid(email):
    body = {"email": email}

    response = requests.post(f"{EMAIL_SERVICE_URL}/api/check/email", json=body)

    try:
        return response.json().get("success")
    except:
        return False
    