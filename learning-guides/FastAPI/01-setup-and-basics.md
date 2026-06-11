# ⚡ Part 1 — Setup & Your First API

> **Time to complete:** ~20 minutes  
> **What you'll have:** A running FastAPI server with 3 working endpoints

← [Back to Overview](./README.md) | [Next: Models & CRUD →](./02-models-and-crud.md)

---

## 🤔 Why FastAPI and Not Flask or Django?

Great question. Here's the honest comparison:

| Feature | FastAPI | Flask | Django REST |
|---|---|---|---|
| Raw Speed | 🚀 Fastest (async-native) | 🐢 Slower | 🐢 Slower |
| Auto Docs | ✅ Built-in, zero config | ❌ Write it yourself | ⚠️ Needs `drf-yasg` plugin |
| Input Validation | ✅ Automatic via Pydantic | ❌ Write it yourself | ⚠️ Serializer boilerplate |
| Type Safety | ✅ First-class | ❌ Optional | ❌ Optional |
| Learning Curve | 🟢 Easy | 🟢 Easy | 🔴 Steep |
| Best For | APIs, microservices | Simple apps, prototypes | Full-stack web apps |

**The sweet spot:** FastAPI gives you Flask's simplicity but with automatic validation, auto-generated interactive docs, and performance that rivals Node.js. For pure API work, it's unbeatable.

---

## 🧠 How FastAPI Works (Big Picture)

Before we write code, here's the mental model:

```
Your Request
     │
     ▼
┌─────────────────────────────────────┐
│  FastAPI receives: POST /tasks      │
│                                     │
│  1. Matches URL to your function    │
│  2. Validates & parses the body     │  ← Pydantic does this
│  3. Calls your function             │
│  4. Serializes the response to JSON │
└─────────────────────────────────────┘
     │
     ▼
JSON Response back to caller
```

You write the function. FastAPI handles everything around it.

---

## 🛠️ Setup in 3 Steps

### Step 1 — Create the project

```bash
mkdir task-api
cd task-api
```

### Step 2 — Create a virtual environment

A virtual environment keeps your project's packages isolated from the rest of your system.

```bash
# Create it
python -m venv venv

# Activate it
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows
```

> 💡 You'll know it's active when you see `(venv)` at the start of your terminal prompt.

### Step 3 — Install FastAPI and Uvicorn

```bash
pip install fastapi uvicorn[standard]
```

- **FastAPI** — the framework itself
- **Uvicorn** — the ASGI server that runs your app (think of it like gunicorn for async Python)

**Save your dependencies:**

```bash
pip freeze > requirements.txt
```

Your project folder should now look like:

```
task-api/
├── venv/            ← don't touch this
└── requirements.txt
```

---

## 🌱 Your First FastAPI App

Create `main.py`:

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI! 🎉"}
```

Run it:

```bash
uvicorn main:app --reload
```

Breaking that command down:
- `main` → the filename (`main.py`)
- `app` → the FastAPI instance inside that file
- `--reload` → auto-restart when you save changes (dev only!)

Open **http://127.0.0.1:8000** → you'll see:

```json
{
  "message": "Hello, FastAPI! 🎉"
}
```

You just built an API. Let's go further.

---

## 🔀 HTTP Methods — The Vocabulary of APIs

Every API endpoint has two parts: **a method** and **a path**.

| Method | Decorator | What it means |
|---|---|---|
| `GET` | `@app.get()` | Fetch/read data |
| `POST` | `@app.post()` | Create new data |
| `PUT` | `@app.put()` | Replace existing data |
| `PATCH` | `@app.patch()` | Update part of existing data |
| `DELETE` | `@app.delete()` | Remove data |

```python
@app.get("/tasks")       # Read all tasks
@app.post("/tasks")      # Create a task
@app.put("/tasks/1")     # Replace task #1
@app.delete("/tasks/1")  # Delete task #1
```

---

## 🛣️ Path Parameters — Dynamic URLs

Path parameters let you capture values from the URL itself.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User #{user_id}"}
```

Call it: `GET /users/42`

Response:
```json
{
  "user_id": 42,
  "name": "User #42"
}
```

**The `: int` matters.** FastAPI automatically validates the type. Try calling `GET /users/hello`:

```json
{
  "detail": [
    {
      "loc": ["path", "user_id"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

No validation code. FastAPI does it for you.

### Multiple path parameters

```python
@app.get("/users/{user_id}/tasks/{task_id}")
def get_user_task(user_id: int, task_id: int):
    return {"user": user_id, "task": task_id}
```

`GET /users/5/tasks/12` → `{"user": 5, "task": 12}`

---

## 🔍 Query Parameters — Filters & Options

Query parameters appear after the `?` in the URL. They're perfect for filtering, sorting, and pagination.

```python
@app.get("/tasks")
def list_tasks(skip: int = 0, limit: int = 10, done: bool = False):
    return {
        "skip": skip,
        "limit": limit,
        "show_done": done
    }
```

| URL | skip | limit | done |
|---|---|---|---|
| `/tasks` | 0 | 10 | False |
| `/tasks?limit=5` | 0 | 5 | False |
| `/tasks?skip=20&limit=5` | 20 | 5 | False |
| `/tasks?done=true` | 0 | 10 | True |

> 💡 **Default values = optional parameter.** No default value = required parameter (caller must provide it).

### Required query parameter

```python
@app.get("/search")
def search(q: str):           # No default → required!
    return {"query": q}
```

`GET /search` → 422 error (missing required param)  
`GET /search?q=python` → `{"query": "python"}`

### Mixing path + query params

```python
@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int, done: bool = False, limit: int = 10):
    return {
        "user": user_id,
        "filter_done": done,
        "limit": limit
    }
```

`GET /users/5/tasks?done=true&limit=3`

---

## 🎯 Putting It All Together

Here's `main.py` with everything from this section:

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    description="Learn FastAPI by building a real app 🚀",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to Task Manager API!", "docs": "/docs"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User #{user_id}"}

@app.get("/tasks")
def list_tasks(skip: int = 0, limit: int = 10, done: bool = False):
    return {
        "skip": skip,
        "limit": limit,
        "show_done": done,
        "tasks": []    # we'll fill this in Part 2!
    }

@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int, done: bool = False, limit: int = 10):
    return {"user": user_id, "done": done, "limit": limit, "tasks": []}
```

Run it and visit **http://127.0.0.1:8000/docs** — you'll see every endpoint documented automatically. Click any endpoint and hit "Try it out" to test it live.

---

## ✅ Checkpoint

By now you should have:

- [x] FastAPI installed and running
- [x] A `GET /` endpoint returning JSON
- [x] Path parameters with type validation
- [x] Query parameters with defaults
- [x] Auto-generated docs at `/docs`

---

## 🧪 Quick Exercises

Try these on your own before moving on:

1. Add a `GET /products/{product_id}` endpoint that returns a product name
2. Add a `GET /search` endpoint with a required `q: str` query param and optional `category: str = "all"`
3. Visit `/docs` and test both endpoints using the Swagger UI

---

← [Back to Overview](./README.md) | [Next: Models & CRUD →](./02-models-and-crud.md)

---

*Part of the [FastAPI Learning Guide](./README.md) · [irshadvaza.tech](https://irshadvaza.tech)*
