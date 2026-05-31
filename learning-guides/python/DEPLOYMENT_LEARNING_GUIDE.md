# 🚀 Python AI App Deployment — Learning Guide

> A step-by-step guide to deploying a Python Streamlit AI app from local VSCode (MacBook) to the cloud — covering two paths: **Streamlit Cloud** (simplest) and **Docker + GitHub + Render** (industry-standard).

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Path A — Streamlit Community Cloud](#path-a--streamlit-community-cloud-recommended-for-beginners)
- [Path B — Docker + GitHub + Render](#path-b--docker--github--render-industry-standard)
- [CI/CD with GitHub Actions](#optional-cicd-with-github-actions)
- [Handling API Keys Securely](#handling-api-keys-securely)
- [Comparison Table](#comparison-table)
- [Common Errors & Fixes](#common-errors--fixes)
- [Useful Resources](#useful-resources)

---

## Prerequisites

Before deploying, make sure you have the following installed on your MacBook:

```bash
# Check Python version (3.9+ recommended)
python3 --version

# Check pip
pip --version

# Check Git
git --version

# Check Docker (for Path B)
docker --version
```

Install anything missing:
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

---

## Project Structure

Organise your project folder like this before deploying:

```
my_ai_app/
├── app.py                  ← Main Streamlit entry point
├── requirements.txt        ← All Python dependencies
├── .env                    ← API keys (NEVER push to GitHub)
├── .gitignore              ← Files to exclude from Git
├── Dockerfile              ← (Path B only) Container definition
├── .github/
│   └── workflows/
│       └── deploy.yml      ← (Optional) GitHub Actions CI/CD
└── README.md               ← Project description
```

### Generate `requirements.txt`

```bash
# Option 1 — Freeze everything installed in your environment
pip freeze > requirements.txt

# Option 2 — Only what your app needs (cleaner, recommended)
pip install pipreqs
pipreqs . --force
```

### Create `.gitignore`

```gitignore
# Environment & secrets
.env
*.env

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
.venv/
venv/
env/

# macOS system files
.DS_Store

# IDE files
.vscode/
.idea/

# Docker
*.log
```

---

## Path A — Streamlit Community Cloud (Recommended for Beginners)

> ✅ No Docker needed · ✅ Free tier · ✅ Live in ~5 minutes

### Step 1 — Prepare your Streamlit app

Make sure your `app.py` runs locally first:

```bash
streamlit run app.py
```

### Step 2 — Push to GitHub

```bash
# Navigate to your project
cd /path/to/my_ai_app

# Initialise Git
git init

# Stage all files
git add .

# First commit
git commit -m "Initial commit: Streamlit AI app"

# Rename branch to main
git branch -M main

# Add your GitHub remote (create an empty repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

> 💡 **Tip:** Create the GitHub repo at [github.com/new](https://github.com/new) — leave it empty (no README, no .gitignore).

### Step 3 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in:
   - **Repository:** your repo
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**

Your app will be live at:
```
https://YOUR_APP_NAME.streamlit.app
```

### Step 4 — Add API Keys (Secrets)

Do **not** put your API keys in code or push `.env` to GitHub.

In the Streamlit Cloud dashboard:
1. Open your app → click **"⋮ Menu"** → **"Settings"**
2. Go to **"Secrets"** tab
3. Paste your keys in TOML format:

```toml
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
SOME_OTHER_KEY = "..."
```

In your `app.py`, read them securely:

```python
import streamlit as st

# Access secrets
api_key = st.secrets["OPENAI_API_KEY"]
anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
```

### Step 5 — Update your deployed app

Every time you push to GitHub, Streamlit Cloud auto-redeploys:

```bash
git add .
git commit -m "Update: improved UI"
git push
```

---

## Path B — Docker + GitHub + Render (Industry Standard)

> 🐳 Learn Docker · 🔁 CI/CD ready · ✅ Free tier on Render · ⏱ ~30 min setup

### Step 1 — Write your Dockerfile

Create a file named `Dockerfile` (no extension) in your project root:

```dockerfile
# ── Base image ──────────────────────────────────────────────
# Use slim Python to keep the image small
FROM python:3.11-slim

# ── Working directory ────────────────────────────────────────
WORKDIR /app

# ── Install dependencies ─────────────────────────────────────
# Copy requirements first — Docker caches this layer
# so rebuilds are fast if only your code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy app source ──────────────────────────────────────────
COPY . .

# ── Expose port ──────────────────────────────────────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ── Run the app ──────────────────────────────────────────────
# --server.address=0.0.0.0 is required so the container
# accepts traffic from outside (the cloud host)
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### Step 2 — Test Docker locally

```bash
# Build the Docker image (run from your project root)
docker build -t my-ai-app .

# Run the container — pass env vars inline for local testing
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  my-ai-app
```

Visit `http://localhost:8501` in your browser. If it works here, it will work in the cloud.

**Useful Docker commands:**

```bash
# List running containers
docker ps

# Stop a running container
docker stop <container_id>

# See all images
docker images

# Remove an image
docker rmi my-ai-app

# View logs
docker logs <container_id>
```

### Step 3 — Push to GitHub

```bash
git add .
git commit -m "Add Dockerfile for containerised deployment"
git push
```

### Step 4 — Deploy on Render (Free)

[Render.com](https://render.com) is the best free platform for Docker deployments.

1. Sign up at [render.com](https://render.com) using your GitHub account
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---|---|
| Environment | Docker |
| Branch | main |
| Region | Choose closest to you |
| Instance Type | Free |

5. Scroll to **"Environment Variables"** and add:

```
OPENAI_API_KEY     →  sk-...
ANTHROPIC_API_KEY  →  sk-ant-...
```

6. Click **"Create Web Service"**

Render will build and deploy your Docker image. Your app will be live at:
```
https://your-app-name.onrender.com
```

> ⚠️ **Free tier note:** Render's free tier spins down after 15 minutes of inactivity. The first visit after sleep takes ~30 seconds to wake up. This is fine for learning and demos.

---

## Optional: CI/CD with GitHub Actions

Automatically redeploy every time you push to `main`.

### Setup

1. In your Render dashboard, go to your service → **"Settings"** → copy the **"Deploy Hook URL"**
2. In GitHub, go to your repo → **"Settings"** → **"Secrets and variables"** → **"Actions"**
3. Add a new secret: `RENDER_DEPLOY_HOOK_URL` → paste the URL

### Create the workflow file

Create `.github/workflows/deploy.yml`:

```yaml
name: 🚀 Deploy to Render

on:
  push:
    branches:
      - main          # triggers on every push to main
  workflow_dispatch:  # allows manual trigger from GitHub UI

jobs:
  deploy:
    name: Trigger Render Deploy
    runs-on: ubuntu-latest

    steps:
      - name: ✅ Checkout code
        uses: actions/checkout@v4

      - name: 🐍 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 📦 Install dependencies
        run: pip install -r requirements.txt

      - name: 🧪 Run basic import test
        run: python -c "import streamlit; print('Streamlit OK')"

      - name: 🚀 Deploy to Render
        run: |
          curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
          echo "Deploy triggered successfully!"
```

Now every `git push origin main` will:
1. Check out your code
2. Install dependencies
3. Run a basic test
4. Trigger Render to rebuild and redeploy

---

## Handling API Keys Securely

| Platform | How to add secrets |
|---|---|
| **Streamlit Cloud** | App Settings → Secrets tab (TOML format) |
| **Render** | Service → Environment → Add env var |
| **GitHub Actions** | Repo Settings → Secrets and variables → Actions |
| **Local dev** | `.env` file (never commit this) |

### Local development with `.env`

```bash
# .env file (gitignored)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

```python
# app.py — works both locally and on Streamlit Cloud
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env locally; use st.secrets on Streamlit Cloud
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
```

Install `python-dotenv`:
```bash
pip install python-dotenv
```

---

## Comparison Table

| Feature | Streamlit Cloud | Docker + Render |
|---|---|---|
| ⏱ Setup time | ~5 minutes | ~30 minutes |
| 🧠 Skills learned | Git, cloud deploy | Docker, CI/CD, containerisation |
| 💰 Free tier | ✅ Yes | ✅ Yes |
| 😴 Sleeps on inactivity | ✅ Yes | ✅ Yes (15 min) |
| 🔄 Auto redeploy on push | ✅ Yes | ✅ Yes (with Actions) |
| 🐳 Docker required | ❌ No | ✅ Yes |
| 🌍 Custom domain | 💲 Paid | 💲 Paid |
| 🔒 Private apps | 1 free | Unlimited |
| 📦 Any framework | ❌ Streamlit only | ✅ Any (Flask, FastAPI…) |
| 🏭 Industry relevance | Medium | High |

**Recommendation:** Start with **Path A** to get online fast, then redo it with **Path B** to build real-world Docker skills.

---

## Common Errors & Fixes

### `ModuleNotFoundError` on deploy

```bash
# Your requirements.txt is missing a package
pip freeze > requirements.txt
git add requirements.txt && git commit -m "fix: update requirements" && git push
```

### `Port already in use` (Docker locally)

```bash
# Find and kill the process using port 8501
lsof -ti:8501 | xargs kill -9

# Or run Docker on a different port
docker run -p 8502:8501 my-ai-app
```

### App crashes with `KeyError` on secrets

```python
# Defensive secret reading — works locally and in cloud
import os
import streamlit as st

def get_secret(key: str) -> str:
    # Try st.secrets first (Streamlit Cloud), then env vars (local/.env)
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Secret '{key}' not found in st.secrets or environment variables")
        return value
```

### Docker build fails on Mac M1/M2/M3 (ARM chip)

```bash
# Build for linux/amd64 (what cloud servers use)
docker buildx build --platform linux/amd64 -t my-ai-app .

# Or add this to your Dockerfile
FROM --platform=linux/amd64 python:3.11-slim
```

### Render deploy stuck / not updating

```bash
# Force a fresh deploy by clearing build cache
# In Render dashboard: Service → Manual Deploy → Clear build cache & deploy
```

---

## Useful Resources

| Resource | Link |
|---|---|
| Streamlit docs | https://docs.streamlit.io |
| Streamlit Community Cloud | https://share.streamlit.io |
| Docker getting started | https://docs.docker.com/get-started/ |
| Render docs | https://render.com/docs |
| GitHub Actions docs | https://docs.github.com/en/actions |
| Python dotenv | https://pypi.org/project/python-dotenv/ |
| pipreqs (clean requirements) | https://pypi.org/project/pipreqs/ |

---

## Learning Milestones Checklist

- [ ] App runs locally with `streamlit run app.py`
- [ ] `.gitignore` created — `.env` is excluded
- [ ] `requirements.txt` generated
- [ ] Code pushed to GitHub
- [ ] App deployed on Streamlit Cloud (Path A)
- [ ] Secrets added securely (not in code)
- [ ] `Dockerfile` written and tested locally
- [ ] Docker image builds and runs on `localhost:8501`
- [ ] App deployed on Render with Docker (Path B)
- [ ] GitHub Actions workflow set up for auto-deploy
- [ ] App auto-redeploys on `git push`

---

*Made for learning purposes · MacBook + VSCode + Streamlit + Python AI apps*
