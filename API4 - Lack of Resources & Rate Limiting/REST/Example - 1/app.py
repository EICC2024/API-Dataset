from pathlib import Path

from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/login")
def login():
    for obj in request.json:
        username = obj.get("username")
        password = obj.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return {"message": "Successfully logged in.!"}

    return {"Invalid username or password.!"}
    