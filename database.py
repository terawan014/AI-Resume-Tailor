import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("resume_history.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                project_input TEXT NOT NULL,
                job_description TEXT NOT NULL,
                resume_markdown TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_resume(name, project_input, job_description, resume_markdown):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO resumes (name, project_input, job_description, resume_markdown)
            VALUES (?, ?, ?, ?)
            """,
            (name, project_input, job_description, resume_markdown),
        )
        return cursor.lastrowid


def get_recent_resumes(limit=10):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, project_input, job_description, resume_markdown, created_at
            FROM resumes
            ORDER BY datetime(created_at) DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def delete_resume(resume_id):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM resumes
            WHERE id = ?
            """,
            (resume_id,),
        )


def update_resume_markdown(resume_id, resume_markdown):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE resumes
            SET resume_markdown = ?
            WHERE id = ?
            """,
            (resume_markdown, resume_id),
        )
