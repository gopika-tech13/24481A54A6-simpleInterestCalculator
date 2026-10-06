import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = 'database.db'

# ---------- DB helpers ----------
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row   # lets us use row['col_name']
    return conn

def init_db():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            email TEXT NOT NULL,
            age   INTEGER
        )
    ''')
    # seed a few rows only if empty
    if conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        conn.executemany(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            [
                ('Ravi',   'ravi@example.com',   25),
                ('Priya',  'priya@example.com',  30),
                ('Arjun',  'arjun@example.com',  22),
            ]
        )
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------

# 1. Show Simple Interest Calculator
@app.route('/', methods=['GET', 'POST'])
def users():

    result = None
    r = None
    t = None
    total = None

    if request.method == 'POST':
        p = float(request.form['p'])
        t = float(request.form['t'])
        r = float(request.form['r'])

        result = (p * t * r) / 100
        total = p + result

    return render_template(
        'index.html',
        result=result,
        r=r,
        t=t,
        total=total
    )


# 2. Show add-user form (GET)
@app.route('/add')
def add_form():
    return render_template('add_user.html')


# 3. Handle add-user submit (CREATE)
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    conn = get_conn()
    conn.execute(
        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
        (name, email, age)
    )
    conn.commit()
    conn.close()

    # After saving, redirect back to calculator
    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug=True)