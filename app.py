from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("database.db")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_user():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = db()
    cur = conn.cursor()

    if role == "student":
        cur.execute("SELECT * FROM students WHERE username=? AND password=?", (username,password))
        if cur.fetchone():
            return redirect("/student_home")

    if role == "staff":
        cur.execute("SELECT * FROM staff WHERE username=? AND password=?", (username,password))
        if cur.fetchone():
            return redirect("/staff_home")

    return "Invalid Login"


@app.route("/student_register")
def student_register():
    return render_template("student_register.html")


@app.route("/staff_register")
def staff_register():
    return render_template("staff_register.html")


@app.route("/register_student", methods=["POST"])
def register_student():

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)
    """,(
        request.form["name"],
        request.form["age"],
        request.form["phone"],
        request.form["district"],
        request.form["mark10"],
        request.form["mark12"],
        request.form["course"],
        request.form["fee"],
        request.form["username"],
        request.form["password"]
    ))

    conn.commit()
    return redirect("/")


@app.route("/register_staff", methods=["POST"])
def register_staff():

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO staff VALUES (?,?,?,?,?,?,?,?)
    """,(
        request.form["college"],
        request.form["location"],
        request.form["district"],
        request.form["contact"],
        request.form["type"],
        request.form["autonomous"],
        request.form["username"],
        request.form["password"]
    ))

    conn.commit()
    return redirect("/")


@app.route("/student_home")
def student_home():
    return render_template("student_home.html")


@app.route("/staff_home")
def staff_home():
    return render_template("staff_home.html")


if __name__ == "__main__":
    app.run(debug=True)
