from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Generate a short random code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()

        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
        conn.commit()
        conn.close()

        return f"Shortened URL: <a href='/{short_code}'>http://localhost:5000/{short_code}</a>"

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return redirect(row[0])
    else:
        return "❌ Short URL not found!", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
