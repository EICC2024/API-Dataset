from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3

app = Flask(__name__)

# Create an empty log file if it doesn't exist
with open('app_log.txt', 'a') as log_file:
    pass

# Function to fetch entries from the database
def get_entries():
    conn = sqlite3.connect('entries.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    entries = cursor.fetchall()
    conn.close()
    return entries

def write_to_log(message):
    with open('app_log.txt', 'a') as log_file:
        log_file.write(message + '\n')

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None  # Initialize the message
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        entries = get_entries()
        for entry in entries:
            if entry[1] == username and entry[3] == password:
                write_to_log(f'Successful login: {username}')
                return redirect(url_for('user_page', username=username))
        
        message = 'Unsuccessful login'  # Set the message for unsuccessful login
    
    return render_template('login.html', message=message)

@app.route('/user/<username>', methods=['GET', 'POST'])
def user_page(username):
    return render_template('user_page.html', username=username)

@app.route('/user/<username>/delete', methods=['POST'])
def delete_user(username):
    conn = sqlite3.connect('entries.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    
    write_to_log(f'Successful delete: {username}')
    flash('Your entry has been deleted.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
