# Setup Guide

[← Data Layer](./05-data-layer.md) · [Interview Q&A →](./07-interview-qa.md)

---

## Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.10+ | `python3 --version` |
| pip | latest | `pip --version` |
| Azure OpenAI resource | — | Azure Portal |
| Azure AI Search resource | — | Azure Portal |
| Parquet file or Azure SQL DB | — | your data |

Optional:
- Azure Content Safety resource (recommended for production)
- LangSmith account (free, for pipeline observability)

---

## Step 1 — Create project folder and virtual environment

### macOS / Linux

```bash
mkdir ~/Projects/SmartSQL
cd ~/Projects/SmartSQL

python3 -m venv .venv
source .venv/bin/activate
# prompt changes to: (.venv) $
```

### Windows

```powershell
mkdir C:\Projects\SmartSQL
cd C:\Projects\SmartSQL

python -m venv .venv
.venv\Scripts\activate
# prompt changes to: (.venv) PS>

# If you see a permissions error on Windows, run first:
# Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

> **Why a virtual environment?**  
> It creates an isolated Python installation for this project. Packages installed here never conflict with other projects. Delete `.venv` and recreate it cleanly at any time.

---

## Step 2 — Copy project files

Place all project files into the folder:

```
SmartSQL/
├── mainui.py
├── llm_langchain.py
├── llm_langgraph.py          (optional — v2 with auto-retry)
├── db_handler.py             (Azure SQL version)
├── db_handler_parquet.py     (DuckDB parquet version)
├── test_steps.py
├── test_parquet.py
├── requirements.txt
└── .env.example
```

---

## Step 3 — Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**What gets installed:**

```
streamlit>=1.35.0          # web UI
langchain>=0.2.0           # AI pipeline framework
langchain-openai>=0.1.0    # Azure OpenAI integration
langchain-core>=0.2.0      # LCEL, Runnables
openai>=1.30.0             # Azure OpenAI SDK
duckdb>=0.10.0             # SQL on parquet files
pandas>=2.2.0              # DataFrames
matplotlib>=3.9.0          # charts
pyodbc>=5.1.0              # Azure SQL driver
SQLAlchemy>=2.0.30         # connection pool
azure-ai-contentsafety>=1.0.0  # content screening
azure-core>=1.30.0         # Azure SDK base
python-dotenv>=1.0.0       # .env loading
```

---

## Step 4 — Configure your .env file

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```bash
# ── Azure OpenAI ──────────────────────────────────────────
# Azure Portal → your OpenAI resource → Keys and Endpoint
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key-here
DEPLOYMENT_NAME=gpt-4o-mini

# ── Embedding model ───────────────────────────────────────
# Deployment name as shown in Azure OpenAI Studio → Deployments
EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002

# ── Azure AI Search ───────────────────────────────────────
# Azure Portal → your Search resource → Overview / Keys
SEARCH_ENDPOINT=https://your-search.search.windows.net
SEARCH_KEY=your-search-key
SEARCH_INDEX_NAME=your-sql-patterns-index

# ── Azure Content Safety (optional) ─────────────────────
CONTENT_SAFETY_ENDPOINT=https://your-cs.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=your-cs-key

# ── Parquet file (for DuckDB version) ────────────────────
# Full absolute path — no ~ shorthand
PARQUET_FILE_PATH=/Users/yourname/Documents/yellow_tripdata_2024-07.parquet
PARQUET_TABLE_NAME=taxi_trips

# ── Azure SQL (for cloud database version) ───────────────
SQL_SERVER=your-server.database.windows.net
SQL_DATABASE=your-database
SQL_USER=your-username
SQL_PASSWORD=your-password
SQL_DRIVER=ODBC Driver 18 for SQL Server

# ── App settings ──────────────────────────────────────────
MAX_ROWS=5000
QUERY_TIMEOUT_SECONDS=30
DEBUG_MODE=true        # set false before going to production

# ── LangSmith (optional — pipeline tracing) ──────────────
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls__your_key
# LANGCHAIN_PROJECT=SmartSQL
```

> **Security:** Never commit `.env` to Git. Run this immediately:
> ```bash
> echo ".env" >> .gitignore
> ```

---

## Step 5 — Run diagnostic tests

### Parquet version

```bash
python test_parquet.py
```

Expected output:
```
=======================================================
  SmartSQL Parquet — component tester
=======================================================

[1] Environment variables
  ✅ PASS  PARQUET_FILE_PATH = /Users/.../yellow_tripdata.parquet

[2] Path security validation
  ✅ PASS  Path validated
  ✅ PASS  Traversal blocked
  ✅ PASS  Wrong extension blocked

[3] Read-only SQL enforcement
  ✅ PASS  valid SELECT
  ✅ PASS  DELETE blocked
  ✅ PASS  DROP blocked

[4] Schema loading
  ✅ PASS  Schema loaded — 19 columns

[5] Row count
  ✅ PASS  Total rows: 7,433,892

[6] Simple SELECT query
  ✅ PASS  Query returned 5 rows, 19 columns

[7] Aggregate query
  ✅ PASS  COUNT result: 7,433,892

[8] LLM SQL generation
  ✅ PASS  SQL generated: SELECT COUNT(*) AS total_trips FROM taxi_trips
```

### LangChain function tests

```bash
python test_steps.py
```

All 12 tests should pass (tests 2, 3, 4, and 11 show BLOCKED — that is correct behaviour showing the safety checks work).

---

## Step 6 — Launch the app

### Parquet version

```bash
streamlit run mainui_parquet.py
```

### Azure SQL version

```bash
streamlit run mainui.py
```

Streamlit opens a browser tab at `http://localhost:8501` automatically.

---

## VS Code setup

1. Open VS Code in the project folder: `code .`
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
3. Type `Python: Select Interpreter`
4. Choose the entry showing `.venv` in the path

VS Code terminal will now activate the environment automatically.

**Recommended extensions:**
- Python (Microsoft)
- Pylance
- Python Debugger

---

## Daily workflow

```bash
# Every time you open a new terminal:
cd ~/Projects/SmartSQL
source .venv/bin/activate          # Mac/Linux
# .venv\Scripts\activate           # Windows

streamlit run mainui_parquet.py    # or mainui.py

# When done:
deactivate
```

---

## Adding new packages

```bash
pip install new-package-name
pip freeze > requirements.txt      # update requirements file
```

Always run `pip freeze` after installing — it records the exact version of every package so others can recreate your environment precisely.

---

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `EnvironmentError: Missing required environment variables` | `.env` not loaded | Check `.env` file is in the same folder as `mainui.py` |
| `ValueError: numpy.dtype size changed` | numpy/pandas binary conflict | `pip uninstall numpy pandas duckdb && pip install numpy==1.26.4 pandas==2.2.2 duckdb==0.10.3` |
| `Invalid embedding endpoint or deployment` | Wrong embedding config | Set `EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002` (not the full URL) |
| `command not found: streamlit` | Virtual env not activated | Run `source .venv/bin/activate` first |
| `The AI service is temporarily unavailable` | Azure API error | Enable `DEBUG_MODE=true` in `.env` to see real error |
| `UserWarning: Parameters {'extra_body'}` | extra_body in model_kwargs | Move to `.bind(extra_body=...)` — already fixed in the provided code |

---

## Azure resource setup checklist

- [ ] Azure OpenAI resource created and GPT-4o-mini deployed
- [ ] text-embedding-ada-002 deployed in the same OpenAI resource
- [ ] Azure AI Search resource created and SQL patterns indexed
- [ ] Azure Content Safety resource created (optional)
- [ ] Azure SQL firewall rules set to allow your IP / App Service outbound IPs
- [ ] `.env` file configured with all keys
- [ ] `.gitignore` includes `.env`
- [ ] `python test_parquet.py` (or `test_steps.py`) shows all green

---

[← Data Layer](./05-data-layer.md) · [Interview Q&A →](./07-interview-qa.md)
