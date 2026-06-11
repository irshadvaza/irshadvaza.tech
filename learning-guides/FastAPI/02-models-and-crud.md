# 📦 Part 2 — Pydantic Models & CRUD

> **Time to complete:** ~30 minutes  
> **What you'll have:** A fully working in-memory Task API with Create, Read, Update, Delete

← [Previous: Setup & Basics](./01-setup-and-basics.md) | [Next: Database →](./03-database.md)

---

## 🤔 What Is Pydantic and Why Do You Care?

Pydantic is the secret weapon behind FastAPI's magic. It lets you describe the **shape** of your data using Python classes — and then it automatically:

- ✅ Validates incoming requests
- ✅ Converts types (e.g. `"42"` → `42`)
- ✅ Generates error messages for bad input
- ✅ Creates the documentation schemas
- ✅ Serializes your response to JSON

You write one class. You get all of that for free.

---

## 🧱 Your First Pydantic Model

```python
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False
```

That's it. `Task` is now a validated data model.

### What each part means

| Part | Meaning |
|---|---|
| `title: str` | Required. Must be a string. |
| `description: Optional[str] = None` | Optional. String or nothing. |
| `done: bool = False` | Optional. Defaults to `False`. |

### Use it in an endpoint

```python
@app.post("/tasks")
def create_task(task: Task):
    return {"message": "Task created!", "task": task}
```

FastAPI sees `task: Task` and knows the request body should match that model. Send a valid request:

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "done": false
}
```

Response:
```json
{
  "message": "Task created!",
  "task": {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "done": false
  }
}
```

Send a bad request (missing `title`):

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Zero validation code written. Pydantic did all of it.** 🎁

---

## 🔢 Adding Validators

Need more control? Pydantic has you covered:

```python
from pydantic import BaseModel, validator, Field
from typing import Optional

class Task(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: int = Field(1, ge=1, le=5)   # 1 to 5
    done: bool = False

    @validator("title")
    def title_must_not_be_blank(cls, v):
        if v.strip() == "":
            raise ValueError("Title cannot be blank")
        return v.strip()
```

| Constraint | Meaning |
|---|---|
| `min_length=3` | String must be at least 3 chars |
| `max_length=100` | String must be at most 100 chars |
| `ge=1` | Number must be ≥ 1 (greater or equal) |
| `le=5` | Number must be ≤ 5 (less or equal) |

---

## 🏗️ Model Inheritance — Reuse, Don't Repeat

A common pattern: you want different shapes for creating vs reading data.

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# What the user sends when creating
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

# What the API returns (includes server-generated fields)
class TaskOut(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True   # Allows reading from SQLAlchemy models (needed in Part 3)
```

`TaskOut` inherits all fields from `TaskCreate` and adds `id` and `created_at`. Clean.

---

## 🏗️ Building the Full CRUD API

Now let's build a real Task API. We'll use an in-memory list for now (the database comes in Part 3).

### The complete `main.py`

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Task Manager API",
    description="A simple API to manage your daily tasks 📋",
    version="1.0.0"
)

# ─────────────────────────────────────────
# Models
# ─────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    done: Optional[bool] = None

class TaskOut(TaskCreate):
    id: int
    created_at: datetime

# ─────────────────────────────────────────
# In-memory "database"
# ─────────────────────────────────────────

tasks: List[TaskOut] = []
counter = 0

def find_task(task_id: int) -> TaskOut:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# ─────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────

# CREATE
@app.post("/tasks", response_model=TaskOut, status_code=201,
          summary="Create a new task")
def create_task(task: TaskCreate):
    global counter
    counter += 1
    new_task = TaskOut(
        id=counter,
        created_at=datetime.utcnow(),
        **task.dict()
    )
    tasks.append(new_task)
    return new_task


# READ ALL
@app.get("/tasks", response_model=List[TaskOut],
         summary="Get all tasks")
def get_tasks(done: Optional[bool] = None, limit: int = 20, skip: int = 0):
    result = tasks
    if done is not None:
        result = [t for t in result if t.done == done]
    return result[skip : skip + limit]


# READ ONE
@app.get("/tasks/{task_id}", response_model=TaskOut,
         summary="Get a single task by ID")
def get_task(task_id: int):
    return find_task(task_id)


# UPDATE (partial — only update fields that are provided)
@app.patch("/tasks/{task_id}", response_model=TaskOut,
           summary="Partially update a task")
def update_task(task_id: int, updates: TaskUpdate):
    task = find_task(task_id)
    updated_data = task.dict()
    for field, value in updates.dict(exclude_unset=True).items():
        updated_data[field] = value
    updated_task = TaskOut(**updated_data)
    tasks[tasks.index(task)] = updated_task
    return updated_task


# DELETE
@app.delete("/tasks/{task_id}", status_code=204,
            summary="Delete a task")
def delete_task(task_id: int):
    task = find_task(task_id)
    tasks.remove(task)
```

---

## 🔍 Breaking Down the Key Parts

### `response_model` — control what gets sent back

```python
@app.post("/tasks", response_model=TaskOut)
```

This tells FastAPI: "Even if my function returns more data, only send back what's in `TaskOut`." Great for hiding sensitive fields (like passwords) from responses.

### `status_code` — set the right HTTP status

```python
@app.post("/tasks", status_code=201)   # 201 Created
@app.delete("/tasks/{id}", status_code=204)  # 204 No Content
```

| Status | Meaning |
|---|---|
| `200` | OK (default) |
| `201` | Created |
| `204` | No Content (delete succeeded, nothing to return) |
| `400` | Bad Request |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

### `exclude_unset=True` — partial updates done right

```python
updates.dict(exclude_unset=True)
```

This is the key to PATCH (partial update). Without it, every unset field would overwrite existing data with `None`. With it, only the fields the user actually sent get applied.

---

## 🧪 Testing Your API

### Option 1 — Swagger UI (easiest)

Visit **http://127.0.0.1:8000/docs**. Every endpoint is there, ready to test with a click.

### Option 2 — curl

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Work through all 5 parts"}'

# Get all tasks
curl http://localhost:8000/tasks

# Get task #1
curl http://localhost:8000/tasks/1

# Mark as done (partial update)
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete task #1
curl -X DELETE http://localhost:8000/tasks/1
```

### Option 3 — HTTPie (more readable than curl)

```bash
pip install httpie

http POST localhost:8000/tasks title="Learn FastAPI"
http GET localhost:8000/tasks
http PATCH localhost:8000/tasks/1 done:=true
http DELETE localhost:8000/tasks/1
```

---

## ⚠️ One Caveat

The in-memory list resets every time you restart the server. **That's fine for learning** — in Part 3 we'll swap it for a real SQLite database so your data actually persists.

---

## ✅ Checkpoint

By now you should have:

- [x] Pydantic models for input and output
- [x] Field validation (min/max length, ranges)
- [x] Model inheritance (`TaskOut` extends `TaskCreate`)
- [x] All 5 CRUD operations working
- [x] Partial updates with PATCH
- [x] Proper HTTP status codes

---

## 🧪 Quick Exercises

1. Add a `priority: int` field (1–5) to `TaskCreate` using `Field`
2. Add a `GET /tasks/stats` endpoint that returns `{"total": N, "done": N, "pending": N}`
3. Try sending a request with `title` as an empty string — see what error you get

---

← [Previous: Setup & Basics](./01-setup-and-basics.md) | [Next: Database →](./03-database.md)

---

*Part of the [FastAPI Learning Guide](./README.md) · [irshadvaza.tech](https://irshadvaza.tech)*
