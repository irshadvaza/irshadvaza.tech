# 03 · 🐍 Python Environment Setup

⬅️ [02 — Azure Setup](./02-azure-ai-foundry-setup.md) | ➡️ Next: [04 — Your First Agent](./04-your-first-agent.md)

---

## 🎯 Goal

Set up the exact same clean, reproducible project layout as the original repo — `uv` for dependency management, a `pyproject.toml`, and a `.env` file — but pointed at Azure packages.

---

## 📦 Step 1 — Install `uv`

`uv` is a fast, modern Python package/dependency manager (a drop-in upgrade over `pip` + `venv`).

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Confirm it's installed:

```bash
uv --version
```

> 🧑‍🎓 **New to `uv`?** Think of it as `pip` + `venv` + `poetry` combined into one fast tool. `uv sync` reads your `pyproject.toml` and creates/updates a virtual environment automatically.

---

## 📁 Step 2 — Project structure

Create the folder that will hold every lesson's code:

```
agentic-ai-azure-course/
 ┣ 📄 main.py                  # Lesson 4 — hello agent
 ┣ 📄 chatbot_agent.py         # Lesson 5–6 — tools + memory
 ┣ 📄 customer_support.py      # Lesson 7 — guardrails + structured output
 ┣ 📄 streamlit_app.py         # Lesson 8 — web UI
 ┣ 📄 multi_agent.py           # Lesson 9 — orchestration
 ┣ 📄 pyproject.toml
 ┣ 📄 .env                     # 🔒 never commit this
 ┣ 📄 .gitignore
 ┗ 📄 uv.lock
```

```bash
mkdir agentic-ai-azure-course && cd agentic-ai-azure-course
uv init --python 3.11
```

---

## 📜 Step 3 — `pyproject.toml`

```toml
[project]
name = "agentic-ai-azure-course"
version = "0.1.0"
description = "Agentic AI crash course rebuilt on Azure AI Foundry + Microsoft Agent Framework"
requires-python = ">=3.11"
dependencies = [
    "agent-framework",
    "agent-framework-azure-ai",
    "azure-identity",
    "azure-ai-projects",
    "python-dotenv",
    "pydantic",
    "streamlit",
]
```

Install everything:

```bash
uv sync
```

| Package | Role in the course |
|---|---|
| `agent-framework` | Core `Agent`, tools, memory, workflows — the Azure-native replacement for the original `agentspan` |
| `agent-framework-azure-ai` | Azure AI Foundry chat client integration |

> 🔄 **Fast-moving SDK notice:** Microsoft Agent Framework is under active development and package/extra names shift between releases (e.g. Foundry support may ship as `agent-framework[foundry]` or as a separate `agent-framework-azure-ai` package). Before installing, check current instructions at **[github.com/microsoft/agent-framework](https://github.com/microsoft/agent-framework)** and adjust the `dependencies` list above accordingly — the import paths used later in this course (`agent_framework`, `agent_framework.foundry`) are correct as of mid-2026 but always verify against the docs.
| `azure-identity` | `AzureCliCredential` / `DefaultAzureCredential` for keyless auth |
| `azure-ai-projects` | Lower-level Foundry project client (used for hosted agents, Bing grounding) |
| `python-dotenv` | Loads `.env` into environment variables |
| `pydantic` | Structured output models (Lesson 7) |
| `streamlit` | Web UI (Lesson 8) |

---

## 🔑 Step 4 — `.env` file

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
BING_CONNECTION_ID=
```

## 🙈 Step 5 — `.gitignore`

```gitignore
.venv/
.env
__pycache__/
*.pyc
.uv/
```

> ⚠️ **Golden rule:** `.env` holds no secrets in this course (we use `az login`, not keys) — but treat it as secret anyway. It's good muscle memory for when you *do* use API keys elsewhere.

---

## 🧪 Step 6 — Verify the environment

Create a throwaway `check_setup.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

required = ["FOUNDRY_PROJECT_ENDPOINT", "AZURE_AI_MODEL_DEPLOYMENT_NAME"]
missing = [key for key in required if not os.getenv(key)]

if missing:
    print(f"❌ Missing env vars: {missing}")
else:
    print("✅ Environment looks good! Ready for Lesson 4.")
```

```bash
uv run python check_setup.py
```

You should see `✅ Environment looks good!`. Delete `check_setup.py` afterward (or keep it — it's a handy sanity check to re-run any time).

---

## 📝 Recap

| Original repo | This course |
|---|---|
| `uv sync` + `pyproject.toml` | ✅ identical workflow |
| `OPENAI_API_KEY` in `.env` | `FOUNDRY_PROJECT_ENDPOINT` + `AZURE_AI_MODEL_DEPLOYMENT_NAME`, auth via `az login` |
| `openai`, `agentspan`, `tavily-agent-toolkit` deps | `agent-framework`, `agent-framework-azure-ai`, `azure-identity` |

➡️ Next: **[04 — Your First Agent](./04-your-first-agent.md)**
