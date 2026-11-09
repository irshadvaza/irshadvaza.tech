# Chapter 3: Setup, tools and costs

> 🎯 **What you will learn**
> - Which accounts and tools you need (and which are free)
> - How to create the three secrets the backend needs
> - How to run the backend and prove it can reach Databricks
> - How to keep your cloud bill small

⏱️ Time: about 60 to 90 minutes the first time. Do it once, then you are ready for every other chapter.

> ⚠️ **Cloud screens change.** Databricks and Azure update their menus often. If a button has moved, search the docs links at the end of each step. The *ideas* stay the same.

---

## 🧸 Before you cook, set up the kitchen

You would not start a recipe without a stove, pans and ingredients. Here:

| Kitchen | This project |
|---|---|
| Stove | **Databricks** (runs the data pipeline and ML) |
| Smart assistant | **Azure OpenAI** (writes explanations) |
| Notebook for your recipe | **GitHub + VS Code** (your code) |
| Pans | **Python** and **Node.js** (run the backend and frontends) |

---

## 1️⃣ Accounts you need

| Account | Needed from | Cost | Notes |
|---|---|---|---|
| **GitHub** | Chapter 3 | Free | Stores the code |
| **Databricks** | Chapter 5 | Free option | Use [Databricks Free Edition](https://www.databricks.com/learn/free-edition) or an [Azure Databricks](https://learn.microsoft.com/azure/databricks/) workspace |
| **Azure** | Chapter 13 | Free trial credit, then pay-as-you-go | Needed for Azure OpenAI and, later, Container Apps |
| **Azure OpenAI access** | Chapter 13 | Pay per use | You create a **model deployment** inside your Azure account |
| **Azure DevOps** *(optional)* | Chapter 17 | Free tier | Only for the CI/CD chapter |

![Databricks workspace](../images/screenshots/ch03-databricks-workspace.png)

> 💡 **Free Edition limits can change.** Read the current limits on the Databricks page before you start. This project is small (about 85,000 rows), so it is designed to fit comfortably.

---

## 2️⃣ Tools to install

| Tool | Version | Used for | Check it |
|---|---|---|---|
| **Git** | any recent | Download and track code | `git --version` |
| **Python** | **3.12 or newer** | Backend, Streamlit, charts | `python --version` |
| **Node.js** | **22 LTS** | React frontend (Vite) | `node --version` |
| **VS Code** | any | Editing | |
| **uv** *(optional)* | latest | Fast Python installer (the backend Dockerfile uses it) | `uv --version` |
| **Docker Desktop** | latest | Chapter 16 only | `docker --version` |
| **Azure CLI** | latest | Chapter 16 only | `az --version` |
| **Databricks CLI** | latest | Chapter 17 only | `databricks --version` |

You only need Git, Python and Node.js today. Install the rest when a chapter asks.

---

## 3️⃣ Get the code

```bash
git clone https://github.com/irshadvaza/azure-ai-data-project-for-everyone.git
cd azure-ai-data-project-for-everyone
```

You now have this map:

```text
databricks/        notebooks 01-07 and the job definition
backend/           FastAPI service
frontend-react/    Frontend A
frontend-streamlit/ Frontend B
data/              the CSV files
docs/              this book
```

---

## 4️⃣ Create the three secrets

The backend needs **three groups of values**. Together they go into one file called `.env`.

> 🔐 **Golden rule:** a `.env` file holds secrets. It is already listed in `.gitignore`, so Git ignores it. **Never** paste a secret into code, a screenshot or a chat. If one leaks, delete it and create a new one.

### Secret group A: connect to the Databricks SQL Warehouse

The **SQL Warehouse** is a small database engine the backend uses to read your Gold tables.

1. In Databricks, open **SQL Warehouses** and create (or open) a **serverless** warehouse. Pick the smallest size.
2. Open its **Connection details** tab. Copy:
   - **Server hostname** → `DATABRICKS_SERVER_HOSTNAME`
   - **HTTP path** → `DATABRICKS_HTTP_PATH`
3. Create a **personal access token (PAT)**: your user menu → **Settings** → **Developer** → **Access tokens** → **Generate new token**. Copy it once (you cannot see it again) → `DATABRICKS_TOKEN`.

![SQL warehouse connection details](../images/screenshots/ch03-sql-warehouse-connection-details.png)

> 📸 *Add your own screenshot above. Cover the token before you save it.*

### Secret group B: control the pipeline from the app

The app can start the Databricks job and upload new files. For that you need:

| Variable | What it is | Where to get it |
|---|---|---|
| `DATABRICKS_JOB_ID` | Number of the job that runs notebooks 01 to 07 | Created in [Chapter 5](05-databricks-setup-and-bronze.md) / [17](17-cicd-and-bundles.md) |
| `DATABRICKS_VOLUME_INCOMING_PATH` | Folder where uploaded CSVs land, e.g. `/Volumes/sales_ai/bronze/raw_files/incoming` | Created by notebook `01` |

You can leave both blank for now and fill them in later. The same token (group A) is used.

### Secret group C: Azure OpenAI

1. In the Azure portal, create an **Azure OpenAI** resource (or an Azure AI Foundry project).
2. Deploy a chat model and give the deployment a name.
3. Copy the **endpoint**, one **key**, and the **deployment name**.

| Variable | Example shape |
|---|---|
| `AZURE_OPENAI_ENDPOINT` | `https://your-resource-name.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | a long random string |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | the name *you* chose when deploying |
| `AZURE_OPENAI_API_VERSION` | `2024-06-01` (the default in the code) |

> 🧠 **Deployment name vs model name.** In Azure OpenAI you call *your deployment's name*, not the model's brand name. If you pick a name like `sales-gpt`, that is what goes in the variable. The code passes it as `model=AZURE_OPENAI_DEPLOYMENT_NAME`.

![Azure OpenAI deployment](../images/screenshots/ch03-azure-openai-deployment.png)

---

## 5️⃣ Create your `.env` file

```bash
cd backend
cp .env.example .env          # Windows PowerShell: copy .env.example .env
```

Open `.env` and fill in the values. The finished file looks like this (fake values):

```ini
DATABRICKS_SERVER_HOSTNAME=dbc-xxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/abc123
DATABRICKS_TOKEN=dapi_your_token_here
DATABRICKS_JOB_ID=123456789
DATABRICKS_VOLUME_INCOMING_PATH=/Volumes/sales_ai/bronze/raw_files/incoming

AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_VERSION=2024-06-01

ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8501
```

`ALLOWED_ORIGINS` is a **CORS** setting: the list of web addresses allowed to call your API from a browser. `5173` is the React dev server, `8501` is Streamlit.

---

## 6️⃣ Run the backend

Still inside the `backend` folder:

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

> ⚠️ **Keep `.env` inside `backend/`.** The code calls `load_dotenv()`, which searches for a file named `.env` starting next to the code and walking up the folders. Always start the backend from `backend/` (`python main.py`).

What each command does:

| Command | Meaning |
|---|---|
| `python -m venv .venv` | Makes a private box for this project's Python packages |
| `source .venv/bin/activate` | Steps into that box |
| `pip install -r requirements.txt` | Installs FastAPI, the Databricks connector, the OpenAI library and more |
| `python main.py` | Starts the API on `http://127.0.0.1:8000` with auto-reload |

---

## ✅ Checkpoint: prove it works

1. Open **<http://localhost:8000/docs>**. You should see the interactive API page (Swagger).
2. Click **GET /health** → **Try it out** → **Execute**.
3. You should see `200` and `"databricks_connected": true`.

![Backend docs page](../images/screenshots/ch03-backend-docs-page.png)

That single green result proves your **token, hostname and HTTP path are all correct**. You do not need any tables yet.

> 🛑 The other endpoints (`/forecast`, `/products`, ...) will return errors until you run the Databricks notebooks in Part 2. That is expected.

---

## 🛠️ Common problems

| Message | Likely cause | Fix |
|---|---|---|
| `DATABRICKS_SERVER_HOSTNAME is missing from .env` | `.env` not found or empty | Put it in `backend/`; check the file name is exactly `.env` (not `.env.txt`) |
| `Could not create a Databricks SQL connection` | Wrong hostname, HTTP path or token, or the warehouse is stopped | Re-copy the values; start the warehouse |
| `/health` takes a long time the first time | Serverless warehouse is waking up | Wait 30 to 60 seconds and retry |
| `ModuleNotFoundError` | Virtual environment not active | Activate `.venv` and re-run `pip install` |
| Browser says *CORS error* later | Your frontend address is not in `ALLOWED_ORIGINS` | Add it (comma-separated) and restart the backend |
| `Missing Azure OpenAI environment variable(s)` | One of the four values is empty | Fill it in; only the explain and chat endpoints need it |

---

## 💰 Keep the cost small

Cloud services bill for *time and usage*. A few habits keep this project cheap:

- 🧹 **Stop or delete what you are not using.** SQL warehouses and clusters cost money while running. Set a short auto-stop.
- 🧪 **Use the smallest sizes.** The data is small. A tiny warehouse is enough.
- 🔢 **Azure OpenAI bills per token** (roughly: per word sent and received). The backend sends a *small fact sheet*, not raw tables, which keeps usage low.
- 😴 **Container Apps can scale to zero** replicas when idle (Chapter 16), so you pay almost nothing between demos.
- 🔔 **Set a budget alert** in Azure: *Cost Management* → *Budgets*. Pick an amount you are comfortable with and an email address.
- 🗑️ **Delete the resource group** when you finish a learning session. Deleting the group deletes everything inside it.

> 💡 **Never guess prices.** They vary by region and change over time. Use the official calculators: [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) and [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

---

## 🔗 Learn more

- [Databricks Free Edition](https://www.databricks.com/learn/free-edition)
- [Create a SQL warehouse](https://learn.microsoft.com/azure/databricks/compute/sql-warehouse/create)
- [Databricks personal access tokens](https://learn.microsoft.com/azure/databricks/dev-tools/auth/pat)
- [Create an Azure OpenAI resource and deploy a model](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)
- [Python virtual environments](https://docs.python.org/3/tutorial/venv.html)
- [uv: fast Python package manager](https://docs.astral.sh/uv/)
- [Node.js downloads](https://nodejs.org/)

⬅️ [Chapter 2](02-big-picture.md) · ➡️ **Next:** [Chapter 4: The data](04-the-data.md)
