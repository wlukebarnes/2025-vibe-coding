from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import os
from services.lists_service import (
    create_todo,
    update_todo,
    change_status,
    list_todos,
    delete_todo,
    get_todo_by_id,
)

router = APIRouter()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoResponse(BaseModel):
    id: int
    user_email: str
    title: str
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str


def get_user_email(request: Request) -> str:
    """Get user email from header or environment variable"""
    # Priority: header first, then env var
    email = request.headers.get("X-Forwarded-Email") or os.getenv("MY_EMAIL")
    if not email:
        raise HTTPException(
            status_code=400, detail="User email not found in headers or environment"
        )
    return email.lower()


@router.post("/todos", response_model=dict)
async def create_todo_endpoint(todo: TodoCreate, request: Request):
    """Create a new todo item"""
    try:
        user_email = get_user_email(request)
        todo_id = create_todo(user_email, todo.title, todo.description or "")
        return {"id": todo_id, "message": "Todo created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create todo: {str(e)}")


@router.put("/todos/{todo_id}", response_model=dict)
async def update_todo_endpoint(todo_id: int, todo: TodoUpdate, request: Request):
    """Update a todo item"""
    try:
        user_email = get_user_email(request)
        success = update_todo(user_email, todo_id, todo.title, todo.description or "")
        if not success:
            raise HTTPException(
                status_code=404, detail="Todo not found or update failed"
            )
        return {"message": "Todo updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")


@router.put("/todos/{todo_id}/status", response_model=dict)
async def change_todo_status(todo_id: int, status: str, request: Request):
    """Change the status of a todo item"""
    try:
        user_email = get_user_email(request)
        success = change_status(user_email, todo_id, status)
        if not success:
            raise HTTPException(
                status_code=404, detail="Todo not found or status update failed"
            )
        return {"message": f"Todo status changed to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to change todo status: {str(e)}"
        )


@router.get("/todos", response_model=List[TodoResponse])
async def list_todos_endpoint(request: Request, include_completed: bool = False):
    """List todo items for the user"""
    try:
        user_email = get_user_email(request)
        rows = list_todos(user_email, include_completed)

        todos = []
        for row in rows:
            todos.append(
                {
                    "id": row[0],
                    "user_email": row[1],
                    "title": row[2],
                    "description": row[3],
                    "status": row[4],
                    "created_at": str(row[5]),
                    "updated_at": str(row[6]),
                }
            )

        return todos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list todos: {str(e)}")


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo_endpoint(todo_id: int, request: Request):
    """Get a single todo item by ID"""
    try:
        user_email = get_user_email(request)
        row = get_todo_by_id(user_email, todo_id)

        if not row:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {
            "id": row[0],
            "user_email": row[1],
            "title": row[2],
            "description": row[3],
            "status": row[4],
            "created_at": str(row[5]),
            "updated_at": str(row[6]),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get todo: {str(e)}")


@router.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo_endpoint(todo_id: int, request: Request):
    """Delete a todo item (mark as deleted)"""
    try:
        user_email = get_user_email(request)
        success = delete_todo(user_email, todo_id)
        if not success:
            raise HTTPException(
                status_code=404, detail="Todo not found or delete failed"
            )
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete todo: {str(e)}")
