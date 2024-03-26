import secrets

from flask import Flask


SECRET_KEY = secrets.token_hex()
LOGIN_SERVICE = "http://localhost:5001"

app = Flask(__name__)


@app.post("/api/login")
def login():
    return {"success": True, "username": "username"}


if __name__ == "__main__":
    app.run("localhost", 5001)
    