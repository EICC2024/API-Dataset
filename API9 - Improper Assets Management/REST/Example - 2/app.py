from pathlib import Path
from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import socket

from config import SECRET_KEY

app = Flask(__name__)
path = Path(__file__)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.post("/api/v1/login")
def post_login():
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            token = jwt.encode({"username": user.username}, app.secret_key, algorithm="HS256")

            return {"message": "Successfully logged in.!", "token": token}
        else:
            return {"error": "Invalid username or password.!"}
    except:
        return {"error": "Unsuccessful login.!"}


@app.post("/api/v2/login")
def post_login_v2():
        try:
            username = request.json.get("username")
            password = request.json.get("password")

            user = User.query.filter_by(username=username).first()
        
            if user and check_password_hash(user.password, password) and ip_address ==('172.17.10.1'):
                token = jwt.encode({"username": user.username}, app.secret_key, algorithm="HS256")

                return {"message" : "Successfully logged in.!", "token": token}
            else:
                return{"error": "Unauthorized Server"'  IP Address:'+ip_address+'  Hostname:'+hostname}

        except:
            return{"error" : "Unsuccessful login.!"}