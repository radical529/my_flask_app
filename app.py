from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('log_hours.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_hours (
        id INTEGER PRIMARY KEY,
        name TEXT,
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
    hours = request.form['hours']

    conn = sqlite3.connect('log_hours.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO log_hours (name, hours) VALUES (?, ?)', (name, hours))
    conn.commit()
    conn.close()

    return redirect('/rank')

@app.route('/rank')
def rank():
    conn = sqlite3.connect('log_hours.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hours FROM log_hours ORDER BY hours DESC')
    log_hours = cursor.fetchall()
    conn.close()

    return render_template('rank.html', log_hours=log_hours)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
