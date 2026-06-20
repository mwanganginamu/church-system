from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # CHANGE if you set password
    database="church_db"
)

cursor = db.cursor()

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")

# REGISTER MEMBER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form.get("email")  # optional
        password = request.form["password"]

        sql = "INSERT INTO members (full_name, phone, email, password) VALUES (%s, %s, %s, %s)"
        val = (name, phone, email, password)
        cursor.execute(sql, val)
        db.commit()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM members WHERE phone=%s AND password=%s", (phone, password))
        user = cursor.fetchone()

        if user:
            session["user"] = user[1]
            return redirect("/admin")
        else:
            return "Invalid login"

    return render_template("login.html")

# ADMIN DASHBOARD
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    cursor.execute("SELECT * FROM prayer_requests")
    prayers = cursor.fetchall()

    return render_template("admin.html", members=members, prayers=prayers)

# PRAYER REQUEST
@app.route("/prayer", methods=["POST"])
def prayer():
    name = request.form["name"]
    message = request.form["message"]

    cursor.execute("INSERT INTO prayer_requests (name, message) VALUES (%s, %s)", (name, message))
    db.commit()

    return redirect("/")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)