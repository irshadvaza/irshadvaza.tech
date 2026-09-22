# 2️⃣ Installation & Setup — Get Your Environment Ready

Before writing any agent code, we need three things ready: **Python**, the **agent-framework** package, and **Azure credentials**. Let's do this slowly, step by step — like setting up a new game console before playing.

## 🪜 Step-by-step setup

```mermaid
flowchart TD
    A["1️⃣ Install Python 3.10+"] --> B["2️⃣ Clone the repo"]
    B --> C["3️⃣ Create a virtual environment"]
    C --> D["4️⃣ pip install -r requirements.txt"]
    D --> E["5️⃣ Set up Azure OpenAI resource"]
    E --> F["6️⃣ Create .env file with your credentials"]
    F --> G["7️⃣ az login (Azure CLI authentication)"]
    G --> H["✅ Ready to run your first agent!"]
```

### Step 1 — Install Python
Download Python 3.10 or newer from [python.org](https://www.python.org/downloads/). Confirm it's installed:

```bash
python --version
```

### Step 2 — Clone the example repository

```bash
git clone https://github.com/Sandesh-hase/Microsoft-Agent-Framework.git
cd Microsoft-Agent-Framework
```

### Step 3 — Create a virtual environment (keeps your project's packages isolated)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 4 — Install the dependencies

The repo's `requirements.txt` lists exactly what you need:

```text
agent-framework
python-dotenv
PyPDF2
pymupdf
```

Install them with:

```bash
pip install -r requirements.txt
```

**What each package does (in plain English):**

| Package | What it's for |
|---|---|
| `agent-framework` | The star of the show — Microsoft's SDK for building and running AI agents |
| `python-dotenv` | Reads secret settings (API keys, endpoints) from a `.env` file so you never hard-code secrets in your script |
| `PyPDF2` / `pymupdf` | Used later to read text out of PDF files (invoices, resumes) so an agent can understand them |

### Step 5 — Create an Azure OpenAI resource

1. Go to the [Azure Portal](https://portal.azure.com).
2. Create an **Azure OpenAI** resource (or use an existing one).
3. Deploy a chat model — the examples in this guide use `gpt-4o-mini`.
4. Note down your **endpoint URL** and the **deployment name**.

> 🆓 **No Azure subscription yet?** You can experiment for free using **GitHub Models** (`https://gh.io/models`), which works with the same Agent Framework APIs — perfect for learning before you commit to a paid Azure resource.

### Step 6 — Create your `.env` file

In the root of your project, create a file named `.env`:

```env
AZURE_OPENAI_ENDPOINT="https://<your-resource-name>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
```

> ⚠️ **Never commit your `.env` file to GitHub!** Add it to `.gitignore` immediately. It's meant to stay private on your machine.

### Step 7 — Choose your authentication method

The framework supports **two** ways to authenticate, and which one you'll actually use depends on your installed version of `agent-framework` and how your Azure resource is set up. Both are valid — pick the one that works for you.

**Option A — API key (simplest, works everywhere):**
Just fill in `AZURE_OPENAI_API_KEY` in your `.env` file as shown above — no extra CLI step needed. Grab the key from your Azure OpenAI resource → **Keys and Endpoint** in the Azure Portal. This is the method used in [Example 1](04-example-1-your-first-agent.md) and is the most reliable starting point if you just want things to run.

**Option B — Azure CLI credential (no key in code, "enterprise" style):**

```bash
az login
```

This lets the framework borrow your signed-in Azure identity via `AzureCliCredential` instead of a pasted key. It's the safer pattern for production, but depending on your package version/class names, you may need `AzureOpenAIChatClient` instead of `OpenAIChatClient` for this to work — see the note in [Example 1](04-example-1-your-first-agent.md) if you hit errors.

> 💡 **Why two methods?** `agent-framework` is a fast-moving, actively developed package (see [Page 1](01-history-and-why-it-exists.md) — it only reached GA in April 2026). Class names and method names have shifted between versions. Always double check `pip show agent-framework` for your installed version if a code sample doesn't match what you see.

## ✅ Sanity check

Create a tiny test script to make sure everything works:

```python
from dotenv import load_dotenv
load_dotenv()

import os
print("Endpoint loaded:", os.getenv("AZURE_OPENAI_ENDPOINT") is not None)
```

If it prints `True`, you're fully set up and ready to build your first agent.

---

⬅️ [Back: History](01-history-and-why-it-exists.md) | ➡️ Next: [Core Concepts & Architecture](03-architecture-and-concepts.md)
