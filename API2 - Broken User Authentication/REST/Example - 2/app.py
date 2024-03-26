from pathlib import Path

from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt

from config import SECRET_KEY


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)


app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = jwt.encode({"username": username}, app.secret_key, algorithm="HS256")

        return {"message": "Successfully logged in.!", "token": token}
    else:
        return {"error": "Invalid username or password.!"}


@app.post("/change-email")
def change_email():
    token = request.json.get("token")
    email = request.json.get("email")

    if token:
        try:
            payload = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        except:
            return {"error": "Please provide a valid token.!"}
    else:
        return {"error": "Token must be provided.!"}

    user = User.query.filter_by(username=payload["username"]).first()

    if user:
        user.email = email

        db.session.commit()

        return {"message": "Successfully changed email.!"}

    return {"Invalid username.!"}
