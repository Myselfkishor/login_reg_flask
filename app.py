from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "kishor_secret_key"

# ------------------ DATABASE HELPER ------------------
def get_db():
    """Connect to the database and ensure 'users' table exists."""
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    con.commit()
    return con, cur

# ------------------ HOME PAGE (REGISTER) ------------------
@app.route('/')
def home():
    return render_template('register.html')

# ------------------ REGISTER ------------------
@app.route('/register', methods=['POST'])
def register():
    uname = request.form.get('uname')
    password = request.form.get('password')

    con, cur = get_db()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE username=?", (uname,))
    existing = cur.fetchone()

    if existing:
        con.close()
        return render_template('register.html', message="User already exists. Try logging in.")

    # Insert new user
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, password))
    con.commit()
    con.close()

    return render_template('login.html', message="Registration successful! Please login.")

# ------------------ LOGIN ------------------
@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    password = request.form.get('password')

    con, cur = get_db()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, password))
    user = cur.fetchone()
    con.close()

    if user:
        session['user'] = uname
        return redirect(url_for('welcome'))
    else:
        return render_template('login.html', message="Invalid username or password")

# ------------------ WELCOME ------------------
@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', uname=session['user'])
    else:
        return redirect(url_for('home'))

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ------------------ LOGIN PAGE ROUTE ------------------
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
