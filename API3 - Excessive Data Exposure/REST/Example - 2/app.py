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
    db_id = db.Column(db.String(5), unique=True)

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


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
        token = jwt.encode({"username": user.username, "id": user.db_id}, app.secret_key, algorithm="HS256")

        return {"message": "Successfully logged in.!", "token": token}
    else:
        return {"error": "Invalid username or password.!"}
    