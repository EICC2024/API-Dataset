from flask import Flask, request

from config import db_context


app = Flask(__name__)


@app.post("/change-password")
@db_context
def login(connection):
    try:
        username = request.json.get("username")
        old_password = request.json.get("old_password")
        new_password = request.json.get("new_password")

        query = "UPDATE user SET password = '{}' WHERE username='{}' and password='{}'"

        connection.execute(query.format(new_password, username, old_password))
        connection.commit()

        return {"message": "User password successfully changed.!"}
    except:
        return {"error": "User not found.!"}
    