from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def get_db_connection():
    connection = sqlite3.connect('mydatabase.db')
    connection.row_factory = sqlite3.Row
    return connection

# Route to display data from the database
@app.route('/')
def index():
    return render_template('index.html')

# Route to show entries
@app.route('/mail/view')
def view_entries():
    try:
        entries_per_page = int(request.args.get('entries', 10))
        page_number = int(request.args.get('page', 1))
        
        connection = get_db_connection()
        cursor = connection.execute('SELECT * FROM users LIMIT ? OFFSET ?', 
                                   (entries_per_page, (page_number - 1) * entries_per_page))
        data = cursor.fetchall()
        connection.close()
        
        return render_template('view_entries.html', data=data, page=page_number, entries=entries_per_page)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
