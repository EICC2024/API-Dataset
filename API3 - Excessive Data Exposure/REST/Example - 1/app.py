from pathlib import Path
from dataclasses import dataclass

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)


@dataclass
class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    db_id: str = db.Column(db.String(5), unique=True)

    username: str = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
db.init_app(app)

with app.app_context():
    db.create_all()


@app.get("/users")
def get_users():
    try:
        return _get_users()
    except:
        return {"error": "An error occured."}


def _get_users():
    return User.query.all()