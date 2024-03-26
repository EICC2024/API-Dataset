from flask import Flask, render_template, request, redirect, url_for

import sqlite3
import random

app = Flask(__name__)

num1 = 0
num2 = 0
correct_answer = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    db_version = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Check if the entered username and password match any database entry
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            global num1, num2, correct_answer
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
            correct_answer = num1 * num2
            return redirect(url_for('multiplication_question'))

        message = "Login failed. Invalid username or password."
        cursor.execute('SELECT sqlite_version()')
        db_version = cursor.fetchone()[0]

        # Close the connection
        conn.close()

    return render_template('index.html', message=message, db_version=db_version)

@app.route('/multiplication', methods=['GET', 'POST'])
def multiplication_question():
    message = ""
    multiplication_question = f"What is {num1} times {num2}?"

    if request.method == 'POST':
        user_answer = request.form.get('answer', type=int)

        if user_answer == correct_answer:
            message = "Correct answer! You are now logged in."
        else:
            message = "Incorrect answer. Please try again."

    return render_template('multiplication.html', message=message, multiplication_question=multiplication_question)

if __name__ == '__main__':
    app.run(debug=False)
