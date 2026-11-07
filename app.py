from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("students.db")

@app.route("/")
def home():
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    roll = request.form["roll"]

    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, roll) VALUES (?, ?)",
        (name, roll)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    app.run(host="0.0.0.0", port=5000)