from flask import Flask, request
import jwt

from config import SECRET_KEY, db_context


app = Flask(__name__)

app.config.from_mapping(SECRET_KEY=SECRET_KEY)


@app.post("/signup")
@db_context
def sigunp(connection):
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        select_query = "SELECT username FROM user WHERE username='{}'"
        insert_query = "INSERT INTO user (username, password) VALUES ('{}', '{}')"

        db_user = connection.executescript(select_query.format(username)).fetchone()

        if not db_user:
            connection.executescript(insert_query.format(username, password))
            connection.commit()

            return {"message": "User successfully created.!"}
        else:
            return {"error": "User already exists.!"}
    except:
        return {"error": "An error occured.!"}
    