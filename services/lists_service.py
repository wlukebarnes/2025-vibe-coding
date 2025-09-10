import os
from typing import List, Tuple, Any
from services.lakebase import Lakebase


def get_schema_from_email(email: str) -> str:
    """Derive schema from email address"""
    return email.split("@")[0].replace(".", "_")


def create_todo(user_email: str, title: str, description: str) -> int:
    """Create a new todo item

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    lakebase = Lakebase()
    schema = get_schema_from_email(user_email.lower())
    table_name = f"{schema}.vibe_coding_lists"

    sql = f"""
    INSERT INTO {table_name} (user_email, title, description, status, created_at, updated_at)
    VALUES ('{user_email.lower()}', '{title}', '{description}', 'pending', NOW(), NOW())
    RETURNING id
    """

    rows = lakebase.query(sql)
    if rows:
        return rows[0][0]
    raise RuntimeError("Failed to create todo item")


def update_todo(user_email: str, todo_id: int, title: str, description: str) -> bool:
    """Update a todo item

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    lakebase = Lakebase()
    schema = get_schema_from_email(user_email.lower())
    table_name = f"{schema}.vibe_coding_lists"

    sql = f"""
    UPDATE {table_name}
    SET title = '{title}', description = '{description}', updated_at = NOW()
    WHERE id = {todo_id} AND user_email = '{user_email.lower()}'
    RETURNING id
    """

    rows = lakebase.query(sql)
    return len(rows) > 0


def change_status(user_email: str, todo_id: int, status: str) -> bool:
    """Change the status of a todo item

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    lakebase = Lakebase()
    schema = get_schema_from_email(user_email.lower())
    table_name = f"{schema}.vibe_coding_lists"

    sql = f"""
    UPDATE {table_name}
    SET status = '{status}', updated_at = NOW()
    WHERE id = {todo_id} AND user_email = '{user_email.lower()}'
    RETURNING id
    """

    rows = lakebase.query(sql)
    return len(rows) > 0


def list_todos(
    user_email: str, include_completed: bool = False
) -> List[Tuple[Any, ...]]:
    """List todo items for a user

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    lakebase = Lakebase()
    schema = get_schema_from_email(user_email.lower())
    table_name = f"{schema}.vibe_coding_lists"

    if include_completed:
        sql = f"""
        SELECT id, user_email, title, description, status, created_at, updated_at
        FROM {table_name}
        WHERE user_email = '{user_email.lower()}'
        ORDER BY created_at DESC
        """
    else:
        sql = f"""
        SELECT id, user_email, title, description, status, created_at, updated_at
        FROM {table_name}
        WHERE user_email = '{user_email.lower()}' AND status != 'deleted'
        ORDER BY created_at DESC
        """

    return lakebase.query(sql)


def delete_todo(user_email: str, todo_id: int) -> bool:
    """Delete a todo item (mark as deleted)

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    return change_status(user_email, todo_id, "deleted")


def get_todo_by_id(user_email: str, todo_id: int) -> Tuple[Any, ...] | None:
    """Get a single todo item by ID

    SECURITY WARNING: Using f-strings instead of parameterized queries for demo purposes.
    This is NOT safe for production use.
    """
    lakebase = Lakebase()
    schema = get_schema_from_email(user_email.lower())
    table_name = f"{schema}.vibe_coding_lists"

    sql = f"""
    SELECT id, user_email, title, description, status, created_at, updated_at
    FROM {table_name}
    WHERE id = {todo_id} AND user_email = '{user_email.lower()}' AND status != 'deleted'
    """

    rows = lakebase.query(sql)
    return rows[0] if rows else None
