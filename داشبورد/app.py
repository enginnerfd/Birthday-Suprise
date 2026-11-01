import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from openai import OpenAI
import csv
import io


app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect("nova.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        
    """)
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    

    conn.commit()
    conn.close()
projects = []


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/assistant")
def ai_assistant():
    return render_template("assistant.html")    
from flask import jsonify
from openai import OpenAI

@app.route("/api/chat", methods=["POST"])
def chat_api():
    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "کلید API تنظیم نشده است."}), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "پیام خالی است."}), 400

    try:
        client = OpenAI()
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions="تو دستیار فارسی‌زبان NOVA هستی. دوستانه، روشن و مفید پاسخ بده.",
            input=message
        )
        return jsonify({"reply": response.output_text})

    except Exception:
        app.logger.exception("NOVA API request failed")
        return jsonify({
            "error": "درخواست هوش مصنوعی ناموفق بود. خطای اصلی را در ترمینال بررسی کن."
        }), 500

@app.route("/analytics")
def analytics():
    conn = get_db_connection()

    total_projects = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    total_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percent = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        progress_percent = 0

    conn.close()

    return render_template(
        "analytics.html",
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress_percent=progress_percent
    )
# @app.route("/projects")
@app.route("/projects", methods=["GET", "POST"])

@app.route("/projects", methods=["GET", "POST"])
def show_projects():
    conn = get_db_connection()

    if request.method == "POST":
        project_name = request.form.get("project_name", "").strip()

        if project_name:
            conn.execute(
                "INSERT INTO projects (name) VALUES (?)",
                (project_name,)
            )
            conn.commit()

        conn.close()
        return redirect(url_for("show_projects"))

    search_query = request.args.get("search", "").strip()

    if search_query:
        projects = conn.execute(
            "SELECT * FROM projects WHERE name LIKE ? ORDER BY id DESC",
            (f"%{search_query}%",)
        ).fetchall()
    else:
        projects = conn.execute(
            "SELECT * FROM projects ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects,
        search_query=search_query
    )


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("show_projects"))

@app.route("/api/stats")
def get_stats():
    conn = get_db_connection()

    total_projects = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    total_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    ).fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percent = round(
            (completed_tasks / total_tasks) * 100
        )
    else:
        progress_percent = 0

    conn.close()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percent": progress_percent
    }


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
@app.route("/tasks", methods=["GET", "POST"])
def manage_tasks():
    conn = get_db_connection()

    if request.method == "POST":
        task_title = request.form.get("task_title", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if task_title:
            conn.execute(
                "INSERT INTO tasks (title, due_date) VALUES (?,?)",
                (task_title,due_date or None)
            )
            conn.commit()

        conn.close()
        return redirect(url_for("manage_tasks"))

    search_query = request.args.get("search", "").strip()

    if search_query:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE title LIKE ? ORDER BY id DESC",
            (f"%{search_query}%",)
        ).fetchall()
    else:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    total_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "tasks.html",
        tasks=tasks,
        total_tasks=total_tasks
    )
@app.route("/tasks/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db_connection()

    task = conn.execute(
        "SELECT completed FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task:
        new_status = 0 if task["completed"] else 1

        conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (new_status, task_id)
        )

        conn.commit()

    conn.close()
    return redirect(url_for("manage_tasks"))
def delete_project(project_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("show_projects"))

@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("manage_tasks"))

@app.route("/tasks/export")
def export_tasks():
    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id DESC"
    ).fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["شناسه", "عنوان وظیفه", "وضعیت"])

    for task in tasks:
        status = "انجام‌شده" if task["completed"] == 1 else "باقی‌مانده"
        writer.writerow([task["id"], task["title"], status])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="nova_tasks.csv"
    )
  
if __name__ == "__main__":
    init_db()
    app.run(debug=True)