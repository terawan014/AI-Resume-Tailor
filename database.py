import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

DB_PATH = Path(__file__).with_name("resume_history.db")


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        secret_value = st.secrets.get(name)
        if secret_value:
            return secret_value
    except Exception:
        pass

    return None


def get_storage_backend():
    if get_secret("SUPABASE_URL") and get_secret("SUPABASE_KEY"):
        return "supabase"
    return "sqlite"


def get_supabase_client():
    if get_storage_backend() != "supabase":
        return None

    from supabase import create_client

    return create_client(
        get_secret("SUPABASE_URL"),
        get_secret("SUPABASE_KEY"),
    )


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if get_storage_backend() == "supabase":
        return

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
    if get_storage_backend() == "supabase":
        client = get_supabase_client()
        response = (
            client.table("resumes")
            .insert(
                {
                    "name": name,
                    "project_input": project_input,
                    "job_description": job_description,
                    "resume_markdown": resume_markdown,
                }
            )
            .execute()
        )
        return response.data[0]["id"]

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
    if get_storage_backend() == "supabase":
        client = get_supabase_client()
        response = (
            client.table("resumes")
            .select("id, name, project_input, job_description, resume_markdown, created_at")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

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
    if get_storage_backend() == "supabase":
        client = get_supabase_client()
        client.table("resumes").delete().eq("id", resume_id).execute()
        return

    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM resumes
            WHERE id = ?
            """,
            (resume_id,),
        )


def update_resume_markdown(resume_id, resume_markdown):
    if get_storage_backend() == "supabase":
        client = get_supabase_client()
        (
            client.table("resumes")
            .update({"resume_markdown": resume_markdown})
            .eq("id", resume_id)
            .execute()
        )
        return

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE resumes
            SET resume_markdown = ?
            WHERE id = ?
            """,
            (resume_markdown, resume_id),
        )
