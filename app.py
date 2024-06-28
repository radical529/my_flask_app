from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Path to the SQLite database file
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_hours.db')

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_hours (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        hours INTEGER
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    hours = int(request.form['hours'])

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute('SELECT hours FROM log_hours WHERE name = ?', (name,))
    result = cursor.fetchone()

    if result:
        # User exists, update their hours
        current_hours = result[0]
        new_hours = current_hours + hours
        cursor.execute('UPDATE log_hours SET hours = ? WHERE name = ?', (new_hours, name))
    else:
        # User does not exist, insert new record
        cursor.execute('INSERT INTO log_hours (name, hours) VALUES (?, ?)', (name, hours))

    conn.commit()
    conn.close()

    return redirect('/rank')

@app.route('/rank')
def rank():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT hours FROM log_hours ORDER BY hours DESC')
    log_hours = cursor.fetchall()
    conn.close()

    return render_template('rank.html', log_hours=log_hours)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
