# ⚡ FastAPI — From Zero to Hero

> Build blazing-fast APIs with Python. No fluff. Just code, clarity, and confidence.

---

## 🗺️ What You'll Build

By the end of this guide, you'll have a fully working **Task Manager API** with:
- ✅ Create, read, update, delete tasks
- ✅ User authentication with JWT tokens
- ✅ Auto-generated interactive docs (free with FastAPI!)
- ✅ Database integration with SQLite

---

## 📚 Table of Contents

1. [Why FastAPI?](#1-why-fastapi)
2. [Setup in 2 Minutes](#2-setup-in-2-minutes)
3. [Your First Endpoint](#3-your-first-endpoint)
4. [Path & Query Parameters](#4-path--query-parameters)
5. [Request Body with Pydantic](#5-request-body-with-pydantic)
6. [CRUD — Build the Task API](#6-crud--build-the-task-api)
7. [Database with SQLAlchemy](#7-database-with-sqlalchemy)
8. [Authentication with JWT](#8-authentication-with-jwt)
9. [Error Handling](#9-error-handling)
10. [Interactive Docs](#10-interactive-docs)
11. [What's Next?](#11-whats-next)

---

## 1. Why FastAPI?

| Feature | FastAPI | Flask | Django REST |
|---|---|---|---|
| Speed | 🚀 Fastest | 🐢 Slower | 🐢 Slower |
| Auto Docs | ✅ Built-in | ❌ Manual | ⚠️ Plugin needed |
| Type Safety | ✅ Yes | ❌ No | ❌ No |
| Learning Curve | Easy | Easy | Steep |

**FastAPI = Flask's simplicity + automatic docs + type validation. It's a no-brainer.**

---

## 2. Setup in 2 Minutes

```bash
# Create a project folder
mkdir task-api && cd task-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install FastAPI + Uvicorn (the server)
pip install fastapi uvicorn[standard]
```

Create a file called `main.py` — that's your entire app for now.

```
task-api/
├── main.py          ← start here
├── venv/
└── requirements.txt
```

---

## 3. Your First Endpoint

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI! 🎉"}
```

**Run it:**

```bash
uvicorn main:app --reload
```

Open your browser: **http://127.0.0.1:8000**

You'll see:
```json
{"message": "Hello, FastAPI! 🎉"}
```

> 💡 `--reload` restarts the server automatically when you save changes. Super handy during development.

---

## 4. Path & Query Parameters

### Path Parameters — part of the URL

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User #{user_id}"}
```

Call it: `GET /users/42` → `{"user_id": 42, "name": "User #42"}`

FastAPI **automatically validates** that `user_id` is an integer. Send a string? It returns a clean error — no extra code needed.

---

### Query Parameters — after the `?`

```python
@app.get("/tasks")
def list_tasks(skip: int = 0, limit: int = 10, done: bool = False):
    return {
        "skip": skip,
        "limit": limit,
        "show_done": done
    }
```

Call it: `GET /tasks?limit=5&done=true`

> 💡 Default values make parameters optional. No default = required parameter.

---

## 5. Request Body with Pydantic

This is where FastAPI really shines. Define the shape of your data once — FastAPI handles validation, serialization, and docs automatically.

```python
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False
```

Use it in an endpoint:

```python
@app.post("/tasks")
def create_task(task: Task):
    return {"message": "Task created!", "task": task}
```

Try sending bad data (e.g., missing `title`):
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

**No validation code written. FastAPI did it for free.** 🎁

---

## 6. CRUD — Build the Task API

Now let's build something real. We'll use an in-memory list first (database comes next).

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Task Manager API")

# --- Model ---
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

class TaskInDB(Task):
    id: int

# --- In-memory "database" ---
tasks_db: List[TaskInDB] = []
task_counter = 0

# --- CREATE ---
@app.post("/tasks", response_model=TaskInDB, status_code=201)
def create_task(task: Task):
    global task_counter
    task_counter += 1
    new_task = TaskInDB(id=task_counter, **task.dict())
    tasks_db.append(new_task)
    return new_task

# --- READ ALL ---
@app.get("/tasks", response_model=List[TaskInDB])
def get_tasks():
    return tasks_db

# --- READ ONE ---
@app.get("/tasks/{task_id}", response_model=TaskInDB)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# --- UPDATE ---
@app.put("/tasks/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, updated: Task):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[i] = TaskInDB(id=task_id, **updated.dict())
            return tasks_db[i]
    raise HTTPException(status_code=404, detail="Task not found")

# --- DELETE ---
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return {"message": "Task deleted ✅"}
    raise HTTPException(status_code=404, detail="Task not found")
```

Test it at **http://127.0.0.1:8000/docs** — you get a full interactive UI!

---

## 7. Database with SQLAlchemy

Time to persist data. Let's swap the list for a real SQLite database.

```bash
pip install sqlalchemy
```

**File structure:**

```
task-api/
├── main.py
├── database.py      ← DB connection
├── models.py        ← DB table definitions
└── schemas.py       ← Pydantic models (request/response shapes)
```

**`database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**`models.py`**

```python
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
```

**`main.py` (updated)**

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import TaskModel
from schemas import TaskCreate, TaskOut
from typing import List

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task Manager API")

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()
```

> 💡 `Depends(get_db)` is FastAPI's **dependency injection** — it automatically handles the DB session lifecycle for every request.

---

## 8. Authentication with JWT

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

**`auth.py`**

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

**Protected endpoint:**

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

@app.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}
```

---

## 9. Error Handling

FastAPI makes error handling clean and consistent:

```python
from fastapi import HTTPException

# Simple error
raise HTTPException(status_code=404, detail="Task not found")

# With extra info
raise HTTPException(
    status_code=422,
    detail={"message": "Validation failed", "field": "title"}
)
```

**Custom exception handler:**

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Task {exc.task_id} doesn't exist. Double-check your ID!"}
    )
```

---

## 10. Interactive Docs

This is FastAPI's magic trick. Just run your app and visit:

| URL | What you get |
|---|---|
| `/docs` | Swagger UI — click and test every endpoint |
| `/redoc` | ReDoc — clean, readable API reference |
| `/openapi.json` | Raw OpenAPI spec (use with Postman, code generators, etc.) |

**Customise your docs:**

```python
app = FastAPI(
    title="Task Manager API",
    description="A simple API to manage your daily tasks 📋",
    version="1.0.0",
    docs_url="/docs",
)
```

---

## 11. What's Next?

You've built a full API. Here's where to go from here:

| Topic | What to learn |
|---|---|
| 🚀 Async | Use `async def` for non-blocking endpoints |
| 🧪 Testing | `pytest` + `TestClient` from FastAPI |
| 🐳 Docker | Containerise and deploy anywhere |
| ☁️ Deploy | Railway, Render, or AWS for free-tier hosting |
| 📦 Background Tasks | `BackgroundTasks` for emails, notifications |
| 🔌 WebSockets | Real-time features with `@app.websocket` |

---

## 📁 Final Project Structure

```
task-api/
├── main.py          ← App entry point & routes
├── database.py      ← DB connection & session
├── models.py        ← SQLAlchemy table models
├── schemas.py       ← Pydantic request/response shapes
├── auth.py          ← JWT authentication helpers
├── tasks.db         ← SQLite database (auto-created)
└── requirements.txt
```

**`requirements.txt`**

```
fastapi
uvicorn[standard]
sqlalchemy
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

---

## 🙌 You Did It!

You went from zero to a production-ready API with auth, a database, validation, and auto-generated docs. Not bad for one guide.

**Star this repo if it helped you →** ⭐

---

*Part of the [Learning Guides](../README.md) series by [@irshadvaza](https://github.com/irshadvaza)*
