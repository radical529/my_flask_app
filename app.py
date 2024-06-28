from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Path to the SQLite database file
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_hours.db')

# Initialize the database
def init_db():
    try:
        print("Initializing database...")
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
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    hours = int(request.form['hours'])

    try:
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
    except sqlite3.Error as e:
        print(f"An error occurred while submitting data: {e}")

    return redirect('/rank')

@app.route('/rank')
def rank():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT name, hours FROM log_hours ORDER BY hours DESC')
        log_hours = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving rank data: {e}")
        log_hours = []

    return render_template('rank.html', log_hours=log_hours)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
