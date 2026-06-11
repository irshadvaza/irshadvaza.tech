# ⚡ FastAPI — From Zero to Hero

> Build blazing-fast APIs with Python. No fluff. Just code, clarity, and confidence.

---

## 🗺️ What You'll Build

By the end of this guide, you'll have a fully working **Task Manager API** with:
- ✅ Create, read, update, delete tasks
- ✅ User authentication with JWT tokens
- ✅ Auto-generated interactive docs (free with FastAPI!)
- ✅ Database integration with SQLite
- ✅ Tests, Docker, and deployment-ready

---

## 📚 Guide Structure

This guide is split into 5 focused parts. Each part builds on the previous one.

| Part | Topic | Time |
|---|---|---|
| [Part 1 — Setup & Basics](./01-setup-and-basics.md) | Install FastAPI, first endpoint, path & query params | ~20 min |
| [Part 2 — Models & CRUD](./02-models-and-crud.md) | Pydantic validation, full Create/Read/Update/Delete | ~30 min |
| [Part 3 — Database](./03-database.md) | SQLAlchemy + SQLite, real persistent storage | ~35 min |
| [Part 4 — Auth & Errors](./04-auth-and-errors.md) | JWT authentication, protected routes, error handling | ~40 min |
| [Part 5 — Docs, Testing & Deploy](./05-docs-and-next-steps.md) | Swagger docs, pytest, Docker, deployment | ~30 min |

**Total: ~2.5 hours** from zero to a production-ready API.

---

## 🚦 Where to Start

**Brand new to FastAPI?** → Start at [Part 1](./01-setup-and-basics.md)

**Know the basics, want to add a database?** → Jump to [Part 3](./03-database.md)

**Want to add login/auth to an existing API?** → Jump to [Part 4](./04-auth-and-errors.md)

---

## 🛠️ What You Need

- Python 3.8 or higher
- Basic Python knowledge (functions, classes, type hints help)
- A terminal and a code editor

---

## 📁 Final Project Structure

By the end of Part 5, your project looks like this:

```
task-api/
├── main.py              ← app entry point
├── database.py          ← DB connection
├── models.py            ← database tables
├── schemas.py           ← request/response shapes
├── crud.py              ← database operations
├── auth.py              ← JWT helpers
├── dependencies.py      ← reusable dependencies
├── routers/
│   ├── users.py         ← auth endpoints
│   └── tasks.py         ← task endpoints
├── tests/
│   └── test_tasks.py    ← automated tests
├── Dockerfile
└── requirements.txt
```

---

## ⚡ Quick Reference

```bash
# Install
pip install fastapi uvicorn[standard]

# Run (with auto-reload)
uvicorn main:app --reload

# View interactive docs
open http://127.0.0.1:8000/docs
```

---

**Star this repo if it helped you →** ⭐

---

*Part of the [Learning Guides](../README.md) series by [@irshadvaza](https://github.com/irshadvaza) · [irshadvaza.tech](https://irshadvaza.tech)*
