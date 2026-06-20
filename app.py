from flask import Flask, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mwangangi1.",
    database="church_db"
)

cursor = db.cursor()

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['user'] = username
            return redirect('/')
        return "Invalid login"

    return '''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="container mt-5">
        <div class="card p-4 shadow" style="max-width:400px;margin:auto;">
            <h3 class="text-center">Admin Login</h3>
            <form method="POST">
                <input class="form-control mb-2" name="username" placeholder="Username">
                <input class="form-control mb-3" name="password" type="password" placeholder="Password">
                <button class="btn btn-primary w-100">Login</button>
            </form>
        </div>
    </div>
    '''

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------------- DASHBOARD ----------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT COUNT(*) FROM members")
    total = cursor.fetchone()[0]

    return f'''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="d-flex">

        <!-- SIDEBAR -->
        <div class="bg-dark text-white p-3 vh-100" style="width:220px;">
            <h4>Church Admin</h4>
            <hr>
            <a class="text-white d-block" href="/">Dashboard</a>
            <a class="text-white d-block" href="/register">Register</a>
            <a class="text-white d-block" href="/members">Members</a>
            <a class="text-white d-block" href="/logout">Logout</a>
        </div>

        <!-- MAIN -->
        <div class="p-4 w-100">

            <h2>Dashboard Overview</h2>

            <div class="row mt-4">

                <div class="col-md-4">
                    <div class="card text-white bg-primary p-3">
                        <h4>Total Members</h4>
                        <h2>{total}</h2>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card text-white bg-success p-3">
                        <h4>System Status</h4>
                        <h2>Active</h2>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card text-white bg-warning p-3">
                        <h4>Admin</h4>
                        <h2>Online</h2>
                    </div>
                </div>

            </div>

        </div>
    </div>
    '''

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
        db.commit()

        return redirect('/members')

    return '''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="container mt-5">
        <div class="card p-4 shadow">
            <h3>Register Member</h3>
            <form method="POST">
                <input class="form-control mb-2" name="name" placeholder="Name">
                <input class="form-control mb-3" name="email" placeholder="Email">
                <button class="btn btn-primary">Save</button>
            </form>
        </div>
    </div>
    '''

# ---------------- MEMBERS ----------------
@app.route('/members')
def members():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()

    rows = ""

    for row in data:
        rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>
                <a class="btn btn-warning btn-sm" href="/edit/{row[0]}">Edit</a>
                <a class="btn btn-danger btn-sm" href="/delete/{row[0]}">Delete</a>
            </td>
        </tr>
        """

    return f'''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="d-flex">

        <div class="bg-dark text-white p-3 vh-100" style="width:220px;">
            <h4>Church Admin</h4>
            <a class="text-white d-block" href="/">Dashboard</a>
            <a class="text-white d-block" href="/register">Register</a>
            <a class="text-white d-block" href="/members">Members</a>
            <a class="text-white d-block" href="/logout">Logout</a>
        </div>

        <div class="p-4 w-100">
            <h2>Members List</h2>

            <table class="table table-bordered table-striped">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
                {rows}
            </table>
        </div>

    </div>
    '''

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("DELETE FROM members WHERE id=%s", (id,))
    db.commit()
    return redirect('/members')

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute("UPDATE members SET name=%s, email=%s WHERE id=%s", (name, email, id))
        db.commit()

        return redirect('/members')

    cursor.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cursor.fetchone()

    return f'''
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="container mt-5">
        <div class="card p-4 shadow">
            <h3>Edit Member</h3>
            <form method="POST">
                <input class="form-control mb-2" name="name" value="{member[1]}">
                <input class="form-control mb-3" name="email" value="{member[2]}">
                <button class="btn btn-success">Update</button>
            </form>
        </div>
    </div>
    '''

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)