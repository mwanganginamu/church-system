from flask import Flask, request, redirect, session

import sqlite3

app = Flask(__name__)
app.secret_key = "church_secret_key"


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect("church.db")
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLE
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# HOME PAGE
@app.route("/")
def home():
    return """
    <h1>Church Management System</h1>

    <p>Welcome to our Church Website</p>

    <a href="/register">Register</a><br><br>
    <a href="/login">Login</a>
    """


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO members (name,email,password) VALUES (?,?,?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            return """
            <h2>Member Registered Successfully</h2>
            <a href='/login'>Login Here</a>
            """

        except:
            return "Email already exists"

    return """
    <h2>Member Registration</h2>

    <form method="POST">

        Name:<br>
        <input type="text" name="name"><br><br>

        Email:<br>
        <input type="email" name="email"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Register">

    </form>
    """


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM members WHERE email=? AND password=?",
            (email, password)
        )

        member = cursor.fetchone()

        conn.close()

        if member:
            session["member_id"] = member["id"]
            session["member_name"] = member["name"]

            return redirect("/dashboard")

        return "Invalid Login Details"

    return """
    <h2>Member Login</h2>

    <form method="POST">

        Email:<br>
        <input type="email" name="email"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">

    </form>
    """


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "member_id" not in session:
        return redirect("/login")

    return f"""
    <h1>Church Dashboard</h1>

    <h3>Welcome {session['member_name']}</h3>

    <ul>
        <li>Prayer Requests</li>
        <li>Events</li>
        <li>Sermons</li>
        <li>Announcements</li>
        <li>Online Donations</li>
    </ul>

    <a href="/logout">Logout</a>
    """


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)