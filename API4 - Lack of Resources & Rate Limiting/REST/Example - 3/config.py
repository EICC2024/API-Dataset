import secrets;

from flask import Flask, request


SECRET_KEY = secrets.token_hex()
EMAIL_SERVICE_URL = "http://localhost:5001"

app = Flask(__name__)


@app.post("/api/check/email")
def check_email():
    email = request.json.get("email")
    print(f"{email} obtained.")

    return {"success": False}


if __name__ == "__main__":
    app.run("localhost", 5001)
