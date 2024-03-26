import secrets
from pathlib import Path
import sqlite3


db_path = Path(__file__).parent / "db.sqlite"

SECRET_KEY = secrets.token_hex()

def db_context(func):
    def inner():
        connection = sqlite3.connect(db_path)
        response = func(connection)
        connection.close()

        return response

    return inner
