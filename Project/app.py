from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "finalproject2024"

DB_FILE = 'quantum_dice_roller.db'


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dice_rolls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        roll_result INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS roll_statistics (
        username TEXT PRIMARY KEY,
        total_rolls INTEGER DEFAULT 0,
        highest_roll INTEGER DEFAULT NULL,
        lowest_roll INTEGER DEFAULT NULL,
        average_roll REAL DEFAULT NULL,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()

def roll_die(min_val=1, max_val=6):
    return (int.from_bytes(os.urandom(1), 'big') % (max_val - min_val + 1)) + min_val

@app.route('/')
def about():
    """Display the about page as the first page."""
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please login instead.")
            return redirect(url_for('login'))

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful. You can now log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for('roll', username=username))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/roll/<username>', methods=['GET', 'POST'])
def roll(username):
    roll_result = None
    if request.method == 'POST':
        try:
            roll_result = roll_die(1, 6)


            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO dice_rolls (username, roll_result) VALUES (?, ?)",
                (username, roll_result)
            )


            cursor.execute('''
                SELECT COUNT(*) AS total_rolls, MAX(roll_result) AS highest_roll, 
                       MIN(roll_result) AS lowest_roll, AVG(roll_result) AS average_roll
                FROM dice_rolls
                WHERE username = ?
            ''', (username,))
            stats = cursor.fetchone()


            cursor.execute('''
                INSERT INTO roll_statistics (username, total_rolls, highest_roll, lowest_roll, average_roll, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET
                    total_rolls = ?,
                    highest_roll = ?,
                    lowest_roll = ?,
                    average_roll = ?,
                    last_updated = CURRENT_TIMESTAMP
            ''', (username, stats['total_rolls'], stats['highest_roll'], stats['lowest_roll'], stats['average_roll'], datetime.now(),
                  stats['total_rolls'], stats['highest_roll'], stats['lowest_roll'], stats['average_roll']))

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error: {e}")
            flash('Error generating dice roll, please try again!', 'error')

    return render_template('roll.html', roll_result=roll_result, username=username)

@app.route('/history/<username>')
def history(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, roll_result, timestamp FROM dice_rolls WHERE username = ? ORDER BY timestamp DESC LIMIT 20", (username,))
    rolls = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('history.html', username=username, rolls=rolls)

@app.route('/statistics/<username>')
def statistics(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_rolls, highest_roll, lowest_roll, average_roll, last_updated FROM roll_statistics WHERE username = ?", (username,))
    stats = cursor.fetchone()
    cursor.close()
    conn.close()

    if stats:
        return render_template(
            'statistics.html', 
            username=username, 
            total_rolls=stats['total_rolls'], 
            highest_roll=stats['highest_roll'], 
            lowest_roll=stats['lowest_roll'], 
            average_roll=round(stats['average_roll'], 2) if stats['average_roll'] else None, 
            last_updated=stats['last_updated']
        )
    else:
        flash("No statistics available. Start rolling to generate stats!", "info")
        return redirect(url_for('roll', username=username))

@app.route('/delete_roll/<username>/<int:roll_id>', methods=['POST'])
def delete_roll(username, roll_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dice_rolls WHERE id = ? AND username = ?", (roll_id, username))
    if cursor.rowcount == 0:
        flash("No such roll found or you are not authorized to delete it.", "error")
    else:
        flash(f"Roll with ID {roll_id} deleted successfully.")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('history', username=username))

@app.route('/logout')
def logout():
    flash("Logged out successfully.")
    return redirect(url_for('register'))

@app.route('/complex_query')
def complex_query():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, AVG(roll_result) AS average_roll, COUNT(*) AS total_rolls
        FROM dice_rolls
        WHERE roll_result >= 4
        GROUP BY username
        HAVING COUNT(*) > 5
    ''')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('complex_query.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
