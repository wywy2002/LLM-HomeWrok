# Task Board FastAPI

## Stack

- Backend: FastAPI
- Frontend: Vanilla HTML/JS
- Persistence: SQLite

## Run

From the repository root:

```powershell
.venv\Scripts\python.exe -m uvicorn week8.task-board-fastapi.app:app --reload
```

Then open `http://127.0.0.1:8000`.

## Features

- Create tasks
- List tasks
- Toggle completion
- Delete tasks

## Notes

- Data is stored in `tasks.db` next to `app.py`.
- This version uses the existing Python environment from the main repository.
