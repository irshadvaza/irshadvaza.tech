# 🔐 Part 4 — Authentication & Error Handling

> **Time to complete:** ~40 minutes  
> **What you'll have:** JWT-secured endpoints, a login flow, clean error handling

← [Previous: Database](./03-database.md) | [Next: Docs & What's Next →](./05-docs-and-next-steps.md)

---

## 🤔 What We're Building

Right now, anyone can call your API. In the real world you need:

1. **Users** — register with an email + password
2. **Login** — exchange credentials for a token
3. **Protected routes** — only work with a valid token

We'll use **JWT (JSON Web Tokens)** — the industry standard for stateless API auth.

---

## 🧠 How JWT Auth Works

```
1. User registers → password stored as a hash (never plain text)

2. User logs in →
   Server verifies password hash →
   Server creates a signed JWT token →
   Returns token to client

3. Client sends token in every request →
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...

4. Server verifies the token signature →
   Extracts user identity →
   Runs the endpoint
```

The token is self-contained — the server doesn't store sessions. Just verify the signature and trust the data inside.

---

## 📦 Install Dependencies

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
pip freeze > requirements.txt
```

- `python-jose` — create and verify JWT tokens
- `passlib[bcrypt]` — hash and verify passwords
- `python-multipart` — required for OAuth2 form-based login

---

## 🧱 New File Structure

```
task-api/
├── main.py
├── database.py
├── models.py        ← add User model
├── schemas.py       ← add User schemas
├── crud.py          ← add user CRUD
├── auth.py          ← NEW: JWT logic
├── dependencies.py  ← NEW: reusable FastAPI dependencies
└── routers/
    ├── tasks.py     ← move task routes here
    └── users.py     ← NEW: register + login + /me
```

---

## Step 1 — `auth.py` — JWT Helpers

```python
# auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# ⚠️ Change this in production! Use an env variable.
SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── Password helpers ─────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Check if plain password matches the stored hash."""
    return pwd_context.verify(plain, hashed)


# ─── Token helpers ────────────────────────────────────────────────

def create_access_token(user_id: int, email: str) -> str:
    """Create a signed JWT token."""
    payload = {
        "sub": str(user_id),    # subject (who the token is for)
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises 401 if invalid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return {"user_id": int(user_id), "email": payload.get("email")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
```

---

## Step 2 — Add the `User` Model

```python
# models.py — add this class
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, index=True, nullable=False)
    password   = Column(String(255), nullable=False)  # stores the hash
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

## Step 3 — User Schemas

```python
# schemas.py — add these classes

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
```

---

## Step 4 — User CRUD

```python
# crud.py — add these functions
from auth import hash_password, verify_password
from models import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email.lower()).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, data: UserRegister) -> User:
    user = User(
        name=data.name,
        email=data.email.lower(),
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
```

---

## Step 5 — `dependencies.py` — The Auth Guard

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_access_token
import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency: extract and validate the current user from the JWT token.
    Inject this into any endpoint you want to protect.
    """
    token_data = decode_access_token(token)
    user = crud.get_user_by_id(db, token_data["user_id"])
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    return user
```

---

## Step 6 — Auth Routes

```python
# routers/users.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserRegister, UserLogin, UserOut, TokenOut
from dependencies import get_current_user
from models import User
import crud
from auth import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists"
        )
    return crud.create_user(db, data)


@router.post("/login", response_model=TokenOut)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(user.id, user.email)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## Step 7 — Protect Task Routes

Now lock down the task endpoints so only logged-in users can use them:

```python
# routers/tasks.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import TaskCreate, TaskUpdate, TaskOut
from dependencies import get_current_user
from models import User
import crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskOut, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected!
):
    return crud.create_task(db, task)


@router.get("", response_model=List[TaskOut])
def get_tasks(
    done: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected!
):
    return crud.get_tasks(db, skip=skip, limit=limit, done=done)
```

---

## Step 8 — Wire It All in `main.py`

```python
# main.py
from fastapi import FastAPI
import models
from database import engine
from routers import tasks, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Secure Task API with JWT auth 🔐",
    version="3.0.0"
)

app.include_router(users.router)
app.include_router(tasks.router)
```

Clean. `main.py` is just 12 lines now.

---

## 🚨 Error Handling

### HTTPException — the standard way

```python
raise HTTPException(status_code=404, detail="Task not found")
raise HTTPException(status_code=409, detail="Email already exists")
raise HTTPException(status_code=401, detail="Not authenticated")
```

### Custom exception classes — for complex apps

```python
# exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, status_code: int, message: str, error_code: str = None):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code

# Register it in main.py:
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code or "ERROR",
            "message": exc.message,
            "path": str(request.url)
        }
    )

# Use it anywhere:
raise AppError(404, "Task not found", "TASK_NOT_FOUND")
```

### Override the default 422 validation error

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(x) for x in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": errors})
```

### Consistent error response format

Pick a format and stick to it:

```json
{
  "error": "TASK_NOT_FOUND",
  "message": "Task 42 does not exist",
  "path": "/tasks/42"
}
```

---

## 🔒 Security Tips

| ✅ Do | ❌ Don't |
|---|---|
| Store SECRET_KEY in environment variables | Hardcode it in your code |
| Use bcrypt for password hashing | Store plain text or MD5 passwords |
| Set short token expiry (1–24 hours) | Make tokens never expire |
| Return 401 for wrong credentials | Return 403 (that leaks info) |
| Use HTTPS in production | Serve over HTTP |

**Reading from environment variables:**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
```

`.env` file:
```
SECRET_KEY=a-very-long-random-string-here
DATABASE_URL=sqlite:///./tasks.db
```

Add `.env` to `.gitignore` — never commit secrets!

---

## 🧪 Testing the Auth Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Irshad", "email": "irshad@example.com", "password": "secret123"}'

# 2. Login → copy the token from the response
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "irshad@example.com", "password": "secret123"}'

# 3. Use the token
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. Create a task (protected)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title": "My first secure task"}'
```

Or just use `/docs` — it has a built-in **Authorize** button (top right) where you paste your token once and it's applied to all requests.

---

## ✅ Checkpoint

By now you should have:

- [x] User registration with hashed passwords
- [x] Login returning a JWT token
- [x] `GET /auth/me` returning the current user
- [x] Protected task endpoints requiring a valid token
- [x] Clean, consistent error handling
- [x] Secrets in environment variables (not hardcoded)

---

## 🧪 Quick Exercises

1. Add a `PATCH /auth/me` endpoint to update the current user's name
2. Add a `POST /auth/logout` endpoint (hint: with JWTs, logout is usually client-side — but explore token blacklisting)
3. Make tasks belong to users — add a `user_id` foreign key to the Task model and only return the current user's tasks

---

← [Previous: Database](./03-database.md) | [Next: Docs & What's Next →](./05-docs-and-next-steps.md)

---

*Part of the [FastAPI Learning Guide](./README.md) · [irshadvaza.tech](https://irshadvaza.tech)*
