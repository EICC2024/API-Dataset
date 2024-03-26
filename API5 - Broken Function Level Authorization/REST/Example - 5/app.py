from pathlib import Path
from dataclasses import dataclass

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import jwt


from config import SECRET_KEY

app = Flask(__name__)
path = Path(__file__)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

db = SQLAlchemy(app)


@dataclass
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username: str = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone: str = db.Column(db.String(15), nullable=False)


with app.app_context():
    db.create_all()


@app.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = jwt.encode({"username": user.username}, app.secret_key, algorithm="HS256")

        return {"message": "Successfully logged in.!", "token": token}
    else:
        return {"error": "Invalid username or password.!"}
    

@app.post("/user")
def get_user_info():
    username = request.json.get("username")
    token = request.json.get("token")

    if jwt.decode(token, app.secret_key, algorithms=["HS256"]):
        return jsonify(User.query.filter_by(username=username).first())
    else:
        return {"error": "Invalid token.!"}
    