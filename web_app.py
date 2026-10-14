import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


CATEGORIES = ("Öneri", "Şikayet", "Geri Bildirim")
STATUSES = ("Yeni", "İnceleniyor", "Tamamlandı")


def create_app(database_path=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-feedback-prototype")
    default_database = Path(__file__).resolve().parent / "instance" / "feedback.sqlite3"
    app.config["DATABASE"] = str(database_path or default_database)

    def connect_database():
        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        return connection

    @contextmanager
    def database():
        connection = connect_database()
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize_database():
        Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
        with database() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    details TEXT NOT NULL,
                    sender TEXT NOT NULL DEFAULT '',
                    email TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Yeni'
                )
                """
            )

    def get_counts(connection):
        counts = {category: 0 for category in CATEGORIES}
        rows = connection.execute(
            "SELECT category, COUNT(*) AS total FROM feedback GROUP BY category"
        ).fetchall()
        counts.update({row["category"]: row["total"] for row in rows if row["category"] in counts})
        return counts

    initialize_database()

    @app.get("/")
    def index():
        with database() as connection:
            counts = get_counts(connection)
            recent_messages = connection.execute(
                "SELECT * FROM feedback ORDER BY id DESC LIMIT 8"
            ).fetchall()
        return render_template(
            "index.html",
            categories=CATEGORIES,
            counts=counts,
            recent_messages=recent_messages,
        )

    @app.post("/feedback")
    def submit_feedback():
        category = request.form.get("category", "").strip()
        title = request.form.get("title", "").strip()
        details = request.form.get("details", "").strip()
        sender = request.form.get("sender", "").strip()
        email = request.form.get("email", "").strip()

        if category not in CATEGORIES or not title or not details:
            flash("Lütfen mesaj türünü, konuyu ve açıklamayı doldurun.", "error")
            return redirect(url_for("index"))

        with database() as connection:
            connection.execute(
                """
                INSERT INTO feedback (category, title, details, sender, email, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (category, title[:160], details[:5000], sender[:120], email[:254], datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
        flash("Mesajınız alındı, teşekkür ederiz.", "success")
        return redirect(url_for("index"))

    @app.get("/inbox")
    def inbox():
        selected_category = request.args.get("category") or None
        with database() as connection:
            counts = get_counts(connection)
            if selected_category:
                rows = connection.execute(
                    "SELECT * FROM feedback WHERE category = ? ORDER BY id DESC",
                    (selected_category,),
                ).fetchall()
            else:
                rows = connection.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
        return render_template(
            "inbox.html",
            categories=CATEGORIES,
            counts=counts,
            selected_category=selected_category,
            messages=rows,
            statuses=STATUSES,
        )

    @app.post("/inbox/<int:message_id>/status")
    def update_status(message_id):
        status = request.form.get("status", "")
        if status in STATUSES:
            with database() as connection:
                connection.execute(
                    "UPDATE feedback SET status = ? WHERE id = ?",
                    (status, message_id),
                )
        return redirect(url_for("inbox", category=request.args.get("category") or None))

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    create_app().run(host="127.0.0.1", port=port)
