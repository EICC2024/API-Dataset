from pathlib import Path

from flask import Flask, request
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests


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


@app.post("/signup")
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    photo_url = request.json.get("photo-url")

    user = User.query.filter_by(username=username).first()

    if not user:
        try:
            path = get_photo(photo_url)
        except:
            return {"error": "Photo couldn't be downloaded.!"}

        user = User(username=username, password=generate_password_hash(password), profile_photo_path=str(path))
        
        db.session.add(user)
        db.session.commit()

        return {"message": "User successfully created.!"}
    else:
        return {"error": "User already exists.!"}



def get_photo(url):
    path = Path(__file__).parent / "images"
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / url.split("/")[-1]
    response = requests.get(url)
    
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path
