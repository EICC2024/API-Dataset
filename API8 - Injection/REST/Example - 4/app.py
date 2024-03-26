from flask import Flask, request
import jwt

from config import SECRET_KEY, db_context


app = Flask(__name__)

app.config.from_mapping(SECRET_KEY=SECRET_KEY)


@app.post("/login")
@db_context
def login(connection):
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        query = "SELECT username, password FROM user WHERE username='{}' and password='{}'"

        db_user = connection.execute(query.format(username, password)).fetchall()[0]

        if db_user:
            token = jwt.encode({"username": db_user}, app.secret_key, algorithm="HS256")

            return {"message": "Successfully logged in.!", "token": token}
        else:
            return {"error": "Invalid username or password.!"}
    except IndexError:
        return {"error": "User not found.!"}
    