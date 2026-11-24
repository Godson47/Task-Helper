"""SQLite persistence for Task Helper.

Set TASK_HELPER_DB to override the default database path, useful for tests and
portable installs. All SQL values are passed as parameters.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

_DEFAULT_DATABASE = Path(__file__).resolve().with_name("tasks.db")
DATABASE_NAME = os.environ.get("TASK_HELPER_DB", str(_DEFAULT_DATABASE))


@contextmanager
def _connection() -> Iterator[sqlite3.Connection]:
    """Open a connection and always close it, rolling back on failures."""
    conn = sqlite3.connect(DATABASE_NAME, timeout=10)
    conn.row_factory = None
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def connect_db() -> sqlite3.Connection:
    """Return a caller-owned connection (kept for backwards compatibility)."""
    return sqlite3.connect(DATABASE_NAME, timeout=10)


def initialize_database() -> None:
    with _connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                description TEXT NOT NULL DEFAULT '',
                due_date TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (status IN ('Pending', 'Completed'))
            )
            """
        )


def add_task(title: str, description: str = "", due_date: str = "") -> None:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Task title cannot be empty.")

    with _connection() as conn:
        conn.execute(
            """INSERT INTO tasks (title, description, due_date, status)
               VALUES (?, ?, ?, 'Pending')""",
            (clean_title, description.strip(), due_date.strip()),
        )


def get_tasks() -> list[tuple]:
    with _connection() as conn:
        return conn.execute(
            """SELECT id, title, description, due_date, status
               FROM tasks ORDER BY id DESC"""
        ).fetchall()


def update_task(task_id: int, title: str, description: str, due_date: str) -> bool:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Task title cannot be empty.")

    with _connection() as conn:
        cursor = conn.execute(
            """UPDATE tasks SET title = ?, description = ?, due_date = ?
               WHERE id = ?""",
            (clean_title, description.strip(), due_date.strip(), task_id),
        )
        return cursor.rowcount > 0


def delete_task(task_id: int) -> bool:
    with _connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0


def toggle_task_status(task_id: int) -> bool:
    with _connection() as conn:
        cursor = conn.execute(
            """UPDATE tasks
               SET status = CASE status
                   WHEN 'Pending' THEN 'Completed'
                   ELSE 'Pending'
               END
               WHERE id = ?""",
            (task_id,),
        )
        return cursor.rowcount > 0
