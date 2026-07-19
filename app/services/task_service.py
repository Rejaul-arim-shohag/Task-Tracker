from typing import Dict, List

from app.database.db import connection
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest


def _ensure_tasks_table() -> None:
    if connection is None:
        raise ValueError("Database connection is not available")

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
    connection.commit()


def create_task(user_id: int, payload: TaskCreateRequest) -> Dict:
    _ensure_tasks_table()

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)",
            (user_id, payload.title, payload.description),
        )
        task_id = cursor.lastrowid
    connection.commit()

    return get_task_by_id(user_id, task_id)


def get_task_by_id(user_id: int, task_id: int) -> Dict:
    _ensure_tasks_table()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, user_id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE id = %s AND user_id = %s
            """,
            (task_id, user_id),
        )
        task = cursor.fetchone()

    if not task:
        raise ValueError("Task not found")

    return task


def get_all_tasks(user_id: int) -> List[Dict]:
    _ensure_tasks_table()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, user_id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,),
        )
        tasks = cursor.fetchall()

    return tasks

