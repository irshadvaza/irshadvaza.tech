# 🚀 Part 5 — Docs, Testing & What's Next

> **Time to complete:** ~30 minutes  
> **What you'll have:** A tested, documented, deployment-ready API

← [Previous: Authentication](./04-auth-and-errors.md) | [Back to Overview →](./README.md)

---

## 📖 Interactive Docs — FastAPI's Best Feature

You've been using `/docs` throughout this guide. Let's make it great.

### The two built-in doc UIs

| URL | Tool | Best for |
|---|---|---|
| `/docs` | Swagger UI | Testing endpoints interactively |
| `/redoc` | ReDoc | Sharing readable API references |
| `/openapi.json` | OpenAPI spec | Importing into Postman, generating client SDKs |

---

### Customise your app metadata

```python
app = FastAPI(
    title="Task Manager API",
    description="""
    ## The Task Manager API

    A clean, fast REST API for managing tasks.

    ### Features
    - ✅ Create, read, update, delete tasks
    - 🔐 JWT-based authentication
    - 📊 Task statistics
    """,
    version="3.0.0",
    contact={
        "name": "Irshad Vaza",
        "url": "https://irshadvaza.tech",
        "email": "hello@irshadvaza.tech"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)
```

### Add tags to group endpoints

```python
# In each router:
router = APIRouter(prefix="/tasks", tags=["Tasks"])
router = APIRouter(prefix="/auth", tags=["Authentication"])
```

This groups your endpoints in the docs — much easier to navigate.

### Document individual endpoints

```python
@router.post(
    "",
    response_model=TaskOut,
    status_code=201,
    summary="Create a new task",
    description="Creates a task and returns it with the generated ID and timestamps.",
    response_description="The newly created task"
)
def create_task(task: TaskCreate, ...):
    ...
```

### Add example values to your Pydantic models

```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

    class Config:
        schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                "description": "Work through the 5-part guide",
                "done": False
            }
        }
```

Now the docs show a real example in the request body editor. Much more helpful than `"string"`.

---

## 🧪 Testing Your API

Tests are how you know your API actually works — and keeps working when you change things.

```bash
pip install pytest httpx
```

### Basic test setup

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
```

`TestClient` runs your FastAPI app in-process — no real server needed. Tests run fast.

### Test the task endpoints

```python
# test_tasks.py
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# ─── Helpers ───────────────────────────────────────────────────────

def register_and_login():
    """Register a test user and return their auth token."""
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ─── Tests ─────────────────────────────────────────────────────────

def test_create_task():
    token = register_and_login()
    response = client.post(
        "/tasks",
        json={"title": "Test task"},
        headers=auth_headers(token)
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["done"] == False
    assert "id" in data


def test_get_tasks():
    token = register_and_login()
    response = client.get("/tasks", headers=auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_task_not_found():
    token = register_and_login()
    response = client.get("/tasks/99999", headers=auth_headers(token))
    assert response.status_code == 404


def test_update_task():
    token = register_and_login()
    # Create
    create_resp = client.post(
        "/tasks",
        json={"title": "Original title"},
        headers=auth_headers(token)
    )
    task_id = create_resp.json()["id"]

    # Update
    update_resp = client.patch(
        f"/tasks/{task_id}",
        json={"done": True},
        headers=auth_headers(token)
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["done"] == True


def test_delete_task():
    token = register_and_login()
    # Create
    create_resp = client.post(
        "/tasks",
        json={"title": "To be deleted"},
        headers=auth_headers(token)
    )
    task_id = create_resp.json()["id"]

    # Delete
    delete_resp = client.delete(f"/tasks/{task_id}", headers=auth_headers(token))
    assert delete_resp.status_code == 204

    # Verify it's gone
    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers(token))
    assert get_resp.status_code == 404


def test_protected_route_without_token():
    response = client.get("/tasks")
    assert response.status_code == 401
```

### Run your tests

```bash
pytest                        # run all tests
pytest -v                     # verbose (shows each test name)
pytest test_tasks.py -v       # run one file
pytest -k "test_create"       # run tests matching a pattern
pytest --tb=short             # shorter tracebacks on failure
```

---

## 🛠️ Middleware — Run Code Around Every Request

Middleware lets you intercept every request before it hits your endpoint and every response before it goes back.

### Logging middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)")
    return response
```

### CORS — allow frontend apps to call your API

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://irshadvaza.tech"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Without this, browsers will block requests from your frontend to your API.

---

## ⚡ Async Endpoints

FastAPI supports `async def` natively. Use it when your endpoint does I/O (calls a DB, an external API, reads files):

```python
import httpx

# ✅ async — non-blocking, handles many requests concurrently
@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://wttr.in/{city}?format=j1")
        return response.json()

# ✅ also fine — sync for simple, CPU-only logic
@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}
```

> 💡 Don't mix: if you use `async def`, use async libraries (`httpx`, `asyncpg`). Calling a blocking library (like `requests`) inside `async def` will freeze your server.

---

## 📦 Background Tasks — Fire and Forget

Need to send an email or run a slow job after responding? Don't make the user wait:

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str):
    # This runs after the response is sent
    print(f"Sending welcome email to {email}...")
    # your email logic here

@router.post("/auth/register", response_model=UserOut, status_code=201)
def register(
    data: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = crud.create_user(db, data)
    background_tasks.add_task(send_welcome_email, user.email)  # non-blocking!
    return user
```

The response goes back to the user immediately. The email sends in the background.

---

## 🐳 Docker — Package Your App

Containerise so it runs the same everywhere:

**`Dockerfile`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

Your API is now at `http://localhost:8000`. Works the same on any machine.

---

## ☁️ Deploy for Free

| Platform | Steps | Best for |
|---|---|---|
| **Railway** | Connect GitHub → click Deploy | Quickest, free tier |
| **Render** | Connect GitHub → set start command | Reliable, free tier |
| **Fly.io** | `fly launch` then `fly deploy` | More control, good free tier |
| **AWS/GCP/Azure** | More setup, more power | Production-grade |

**Railway (easiest):**

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables (SECRET_KEY, DATABASE_URL)
4. Done — live URL in 2 minutes

---

## 🗺️ What to Learn Next

You've built a production-grade API. Here's the honest roadmap of what comes after:

### Level up your FastAPI

| Topic | Why it matters |
|---|---|
| **WebSockets** | Real-time features (chat, notifications, live updates) |
| **File uploads** | Handle images, PDFs with `UploadFile` |
| **Pagination** | Cursor-based pagination for large datasets |
| **Rate limiting** | Protect your API from abuse with `slowapi` |
| **Caching** | Redis for fast repeated reads |

### Go deeper on architecture

| Topic | Why it matters |
|---|---|
| **Alembic** | Database migrations — change your schema without losing data |
| **Celery** | Heavy background jobs (image processing, report generation) |
| **PostgreSQL** | Production-grade database (swap SQLite in one line) |
| **Docker Compose** | Run API + DB + Redis together locally |

### Testing and quality

| Topic | Why it matters |
|---|---|
| **pytest fixtures** | Share setup across tests cleanly |
| **Test database** | Isolated DB per test run |
| **Coverage** | `pytest --cov` to see what's untested |

---

## 📁 Final Project Structure

Here's the full structure of what we built across all 5 parts:

```
task-api/
├── main.py              ← app entry point, middleware, router registration
├── database.py          ← SQLAlchemy engine & get_db dependency
├── models.py            ← User and Task table definitions
├── schemas.py           ← Pydantic input/output models
├── crud.py              ← all database operations
├── auth.py              ← JWT create/decode, password hash/verify
├── dependencies.py      ← get_current_user dependency
├── routers/
│   ├── users.py         ← /auth/register, /auth/login, /auth/me
│   └── tasks.py         ← /tasks CRUD (protected)
├── tests/
│   ├── test_tasks.py
│   └── test_auth.py
├── tasks.db             ← SQLite file (auto-created)
├── .env                 ← secrets (never commit this!)
├── .gitignore
├── Dockerfile
└── requirements.txt
```

---

## 🎓 You Finished the Guide!

Here's what you built and learned across all 5 parts:

| Part | What you learned |
|---|---|
| 1 | Setup, HTTP methods, path params, query params |
| 2 | Pydantic models, validation, full CRUD |
| 3 | SQLAlchemy, real database, dependency injection |
| 4 | JWT auth, protected routes, error handling |
| 5 | Docs, testing, async, background tasks, deployment |

That's a production-grade API. Not a toy. Not a tutorial project. Something you could deploy today.

**If this helped you, star the repo ⭐ and share it with someone learning Python.**

---

← [Previous: Authentication](./04-auth-and-errors.md) | [Back to Overview →](./README.md)

---

*Part of the [FastAPI Learning Guide](./README.md) · [irshadvaza.tech](https://irshadvaza.tech)*
