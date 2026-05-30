from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"

app = FastAPI(title="Task Board FastAPI")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    details: str = Field(default="", max_length=500)


class TaskUpdate(TaskCreate):
    completed: bool


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


def row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "details": row["details"],
        "completed": bool(row["completed"]),
    }


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (BASE_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/api/tasks")
def list_tasks() -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT id, title, details, completed FROM tasks ORDER BY id DESC").fetchall()
    return [row_to_task(row) for row in rows]


@app.post("/api/tasks", status_code=201)
def create_task(payload: TaskCreate) -> dict[str, Any]:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, details, completed) VALUES (?, ?, 0)",
            (payload.title.strip(), payload.details.strip()),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, title, details, completed FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return row_to_task(row)


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate) -> dict[str, Any]:
    with get_conn() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET title = ?, details = ?, completed = ? WHERE id = ?",
            (payload.title.strip(), payload.details.strip(), int(payload.completed), task_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
        row = conn.execute(
            "SELECT id, title, details, completed FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    return row_to_task(row)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()

