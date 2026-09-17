import sqlite3

DATABASE_NAME = "tasks.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_task(title, description, due_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, status)
        VALUES (?, ?, ?, 'Pending')
    """, (title, description, due_date))

    conn.commit()
    conn.close()


def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, due_date, status
        FROM tasks
        ORDER BY id DESC
    """)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id, title, description, due_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?
        WHERE id = ?
    """, (title, description, due_date, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def toggle_task_status(task_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM tasks WHERE id = ?",
        (task_id,)
    )
    result = cursor.fetchone()

    if result:
        new_status = "Completed" if result[0] == "Pending" else "Pending"

        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (new_status, task_id))

    conn.commit()
    conn.close()
