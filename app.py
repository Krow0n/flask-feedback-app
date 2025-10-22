from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"  # Required for flash messages


# 🧩 Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# 🏠 Home Page — Submit Feedback
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        feedback = request.form["feedback"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO feedback (name, feedback) VALUES (?, ?)", (name, feedback))
        conn.commit()
        conn.close()

        flash("Feedback submitted successfully!", "success")
        return redirect(url_for("view_feedback"))

    return render_template("index.html")


# 📋 View All Feedback
@app.route("/view_feedback")
def view_feedback():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, name, feedback FROM feedback")
    feedbacks = c.fetchall()
    conn.close()
    return render_template("view_feedback.html", feedbacks=feedbacks)


# ✏️ Edit Feedback
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_feedback(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        feedback = request.form["feedback"]
        c.execute("UPDATE feedback SET name = ?, feedback = ? WHERE id = ?", (name, feedback, id))
        conn.commit()
        conn.close()
        flash("Feedback updated successfully!", "success")
        return redirect(url_for("view_feedback"))

    c.execute("SELECT name, feedback FROM feedback WHERE id = ?", (id,))
    record = c.fetchone()
    conn.close()

    if record:
        return render_template("edit_feedback.html", id=id, feedback={"name": record[0], "feedback": record[1]})
    else:
        flash("Feedback not found!", "danger")
        return redirect(url_for("view_feedback"))


# ❌ Delete Feedback
@app.route("/delete/<int:id>")
def delete_feedback(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Feedback deleted successfully!", "danger")
    return redirect(url_for("view_feedback"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
