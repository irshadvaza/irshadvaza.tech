# 🗄️ Part 3 — Database with SQLAlchemy

> **Time to complete:** ~35 minutes  
> **What you'll have:** A Task API backed by a real SQLite database — data persists across restarts

← [Previous: Models & CRUD](./02-models-and-crud.md) | [Next: Authentication →](./04-auth-and-errors.md)

---

## 🤔 Why a Database?

The in-memory list from Part 2 is great for learning, but it has one big problem: **restart the server and all your data vanishes**.

A real database fixes that. We'll use:

- **SQLite** — a lightweight file-based database, zero config, perfect for dev and small projects
- **SQLAlchemy** — the most popular Python ORM (Object Relational Mapper), lets you work with tables as Python classes
- **FastAPI's dependency injection** — cleanly manages database sessions per request

---

## 🧠 The Big Picture

```
HTTP Request
     │
     ▼
FastAPI Endpoint
     │
     ├── Pydantic schema validates the input
     │
     ├── get_db() provides a database session
     │
     ├── SQLAlchemy queries/writes to tasks.db
     │
     └── Response schema shapes the output
          │
          ▼
     JSON Response
```

---

## 📁 New File Structure

We're splitting the code into focused files:

```
task-api/
├── main.py          ← routes/endpoints
├── database.py      ← DB engine & session factory
├── models.py        ← SQLAlchemy table definitions
├── schemas.py       ← Pydantic input/output models
├── crud.py          ← database operations (create, read, update, delete)
├── tasks.db         ← SQLite file (auto-created on first run)
└── requirements.txt
```

> 💡 This separation keeps each file small and focused. `main.py` only handles routing. DB logic lives in `crud.py`. Much easier to maintain.

---

## 🔧 Install SQLAlchemy

```bash
pip install sqlalchemy
pip freeze > requirements.txt
```

---

## Step 1 — `database.py` — Connection & Session

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite file path — the file gets created automatically
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific, needed for FastAPI
)

# Session factory — creates new DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our table models
Base = declarative_base()


# Dependency — provides a DB session, closes it after the request
def get_db():
    db = SessionLocal()
    try:
        yield db         # FastAPI uses the session here
    finally:
        db.close()       # Always close, even if an error occurred
```

### What is `yield` doing here?

`get_db` is a **generator function**. FastAPI calls it before your endpoint runs, injects the `db` session, then resumes after `yield` to close it — even if an exception was raised. It's like a `try/finally` wrapped around your entire endpoint automatically.

---

## Step 2 — `models.py` — Database Tables

```python
# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    done        = Column(Boolean, default=False, nullable=False)
    priority    = Column(Integer, default=1, nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())
```

Each class = one database table. Each class attribute = one column.

| SQLAlchemy Type | Python Type | Example |
|---|---|---|
| `Integer` | `int` | `42` |
| `String(n)` | `str` | `"hello"` |
| `Boolean` | `bool` | `True` |
| `DateTime` | `datetime` | `2024-01-15 10:30:00` |
| `Float` | `float` | `3.14` |

---

## Step 3 — `schemas.py` — Pydantic Models

These are separate from the SQLAlchemy models. Pydantic schemas define the **API contract** (what comes in, what goes out). SQLAlchemy models define the **database structure**.

```python
# schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# What the user sends to CREATE a task
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    done: bool = False
    priority: int = Field(1, ge=1, le=5)

# What the user sends to UPDATE a task (all fields optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)

# What the API sends BACK (includes server-generated fields)
class TaskOut(TaskCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True   # Allows reading from SQLAlchemy model instances
```

> 💡 `orm_mode = True` is crucial. Without it, Pydantic can't read data from SQLAlchemy objects (which are lazy-loaded, not plain dicts).

---

## Step 4 — `crud.py` — Database Operations

Keep all DB queries in one place. Clean, testable, reusable.

```python
# crud.py
from sqlalchemy.orm import Session
from typing import Optional, List
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    done: Optional[bool] = None
) -> List[Task]:
    query = db.query(Task)
    if done is not None:
        query = query.filter(Task.done == done)
    return query.offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Reload from DB to get generated fields (id, created_at)
    return db_task


def update_task(db: Session, task_id: int, updates: TaskUpdate) -> Optional[Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def get_stats(db: Session) -> dict:
    total = db.query(Task).count()
    done = db.query(Task).filter(Task.done == True).count()
    return {"total": total, "done": done, "pending": total - done}
```

---

## Step 5 — `main.py` — Clean Routes

With all logic extracted, `main.py` is beautifully slim:

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import models, crud
from database import engine, get_db
from schemas import TaskCreate, TaskUpdate, TaskOut

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A real API with a real database 🗄️",
    version="2.0.0"
)


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(
    done: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return crud.get_tasks(db, skip=skip, limit=limit, done=done)


@app.get("/tasks/stats")
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
```

---

## 🔍 Understanding `Depends(get_db)`

```python
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
```

`Depends(get_db)` is FastAPI's **dependency injection** system. Here's what happens:

1. A request hits `POST /tasks`
2. FastAPI calls `get_db()` → opens a DB session
3. Injects that session as `db` into your function
4. Your function runs
5. FastAPI resumes `get_db()` after the `yield` → closes the session

You never manually open or close sessions. FastAPI handles the lifecycle. This also means sessions are never leaked, even when exceptions occur.

---

## 🏃 Run It

```bash
uvicorn main:app --reload
```

On first run, FastAPI creates `tasks.db` automatically. Add some tasks, restart the server — your data is still there! 🎉

---

## 🔎 Inspect the Database (Optional)

Want to see the raw SQLite data?

```bash
# Install the SQLite CLI (if not already installed)
# macOS: brew install sqlite
# Ubuntu: sudo apt install sqlite3

sqlite3 tasks.db

# Inside SQLite shell:
.tables             -- list all tables
.schema tasks       -- show table structure
SELECT * FROM tasks;
.quit
```

Or use a GUI tool like [DB Browser for SQLite](https://sqlitebrowser.org/) — free and excellent.

---

## 🔄 Switching to PostgreSQL (When You're Ready)

SQLite is great for development. For production, switch to PostgreSQL with one line change:

```bash
pip install psycopg2-binary
```

```python
# database.py — just change this line:
DATABASE_URL = "postgresql://user:password@localhost/taskdb"

# Remove the connect_args (SQLite-specific):
engine = create_engine(DATABASE_URL)
```

Everything else stays the same. That's the beauty of SQLAlchemy.

---

## ✅ Checkpoint

By now you should have:

- [x] SQLAlchemy connected to SQLite
- [x] Separate files for models, schemas, crud, routes
- [x] Data persists across server restarts
- [x] Dependency injection managing DB sessions
- [x] Stats endpoint

---

## 🧪 Quick Exercises

1. Add a `due_date: Optional[datetime]` column to the Task model
2. Add a `GET /tasks?priority=5` filter in `get_tasks`
3. Add a `GET /tasks/overdue` endpoint that returns tasks where `due_date < now` and `done == False`

---

← [Previous: Models & CRUD](./02-models-and-crud.md) | [Next: Authentication →](./04-auth-and-errors.md)

---

*Part of the [FastAPI Learning Guide](./README.md) · [irshadvaza.tech](https://irshadvaza.tech)*
