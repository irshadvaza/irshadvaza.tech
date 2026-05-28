# 📓 Notebook: Bronze & Silver Agentic Pipeline
### AI-Powered Data Ingestion & Cleaning | Azure Databricks + GPT-4o-mini

> **Notebook:** `notebooks/01_bronze_silver_agent.py`  
> **Layer:** Bronze (Raw Ingestion) → Silver (AI-Cleaned Data)  
> **AI Model:** Azure OpenAI GPT-4o-mini  
> **Compute:** Azure Databricks (Unity Catalog)

---

## 📋 What This Notebook Does

This notebook implements **two autonomous AI agents** that handle the first two layers of the Medallion architecture — **without any hardcoded transformation logic.**

```
CSV Files in ADLS Volume
        │
        ▼
┌───────────────────────┐
│  🤖 Bronze Loader     │  ← AI generates PySpark to ingest any CSV
│     Agent             │    → Writes raw Delta tables
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  🤖 Silver Cleaning   │  ← AI reads schema + sample data
│     Agent             │    → Decides what cleaning is needed
└───────────┬───────────┘    → Writes cleaned Delta tables
            │
            ▼
     Silver Delta Tables
     (Business-ready data)
```

**Key capability:** Both agents **self-heal** — if the generated PySpark code fails at runtime, the error is automatically sent back to the AI which rewrites the code and retries.

---

## 🏗 Unity Catalog Structure

```
env_data  (Catalog)
├── bronze  (Schema)
│   ├── [table_1]   ← Raw CSV → Delta (written by Bronze Agent)
│   ├── [table_2]
│   └── [table_N]
│
├── silver  (Schema)
│   ├── [table_1]   ← Cleaned data (written by Silver Agent)
│   ├── [table_2]
│   └── [table_N]
│
└── Volumes
    └── raw_data/   ← CSV files dropped here → auto-ingested
```

---

## 🔐 Security Setup — Do This Before Running

> **⚠️ NEVER hardcode API keys in notebooks you commit to GitHub.**  
> Use Databricks Secrets instead — here's exactly how:

### Step 1: Store your key in Databricks Secret Scope

```bash
# Run this in Databricks CLI (one time only)
databricks secrets create-scope --scope ai-secrets
databricks secrets put --scope ai-secrets --key openai-api-key
# → paste your Azure OpenAI key when prompted
```

### Step 2: Use the secret in your notebook

```python
# ✅ SAFE — key is never visible in code or logs
api_key = dbutils.secrets.get(scope="ai-secrets", key="openai-api-key")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-12-01-preview",
    azure_endpoint="https://your-resource.openai.azure.com/"
)
```

This way, even if someone sees your notebook on GitHub, **the key is not there.**

---

## 🧩 Cell-by-Cell Code Walkthrough

---

### ✅ Cell 1 — Azure OpenAI Client Setup

```python
from openai import AzureOpenAI

# ✅ Production version — use Databricks secrets (see Security Setup above)
api_key = dbutils.secrets.get(scope="ai-secrets", key="openai-api-key")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-12-01-preview",
    azure_endpoint="https://ai-yourresource.openai.azure.com/"
)
```

**What it does:**
Initialises the Azure OpenAI client using the `AzureOpenAI` SDK class. The `api_version` here targets the latest GA preview endpoint, which supports `gpt-4o-mini` — a fast, cost-efficient model ideal for code generation tasks.

**Why `gpt-4o-mini`?**
- Generates valid PySpark code reliably
- Much cheaper than GPT-4 (important — this agent calls the API on every retry)
- Fast response time keeps the pipeline latency low

---

### ✅ Cell 2 — `call_llm()` — The AI Communication Layer

```python
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content.strip()

    # ── Hard clean the response ──────────────────────────────────
    # LLMs sometimes prefix output with "python" or wrap in ```python
    # blocks. Both would break exec() — so we strip them aggressively.

    if content.lower().startswith("python"):
        content = content[len("python"):].strip()

    content = content.replace("```python", "").replace("```", "").strip()

    return content
```

**What it does:**
A reusable wrapper around the Azure OpenAI chat API. Every agent in this pipeline calls this function — it handles the API call and **sanitises the output** before returning it.

**Why the hard cleaning matters:**
LLMs frequently return code wrapped in markdown fences like ` ```python ... ``` ` or prefixed with the word "python". If you pass that directly to `exec()`, Python throws a `SyntaxError` because ` ```python ` is not valid Python. The three-line clean block prevents this from ever failing.

---

### ✅ Cell 3 — `bronze_loader_agent()` — The Ingestion Brain

```python
def bronze_loader_agent(volume_path, catalog, schema, max_retries=3):
    
    print("\nRunning Bronze Loader Agent...")
    print("Volume Path:", volume_path)

    # ── Prompt 1: Generate the ingestion code ────────────────────
    base_prompt = f"""
    You are a senior data engineer working in Databricks.
    Generate ONLY valid PySpark code.

    Task:
    - Read all CSV files from: {volume_path}
    - Use dbutils.fs.ls()
    - Loop through files
    - Extract table name (remove .csv, lowercase)
    - Load CSV (header=True, inferSchema=True)
    - Write RAW data to Delta tables
    - Delete from the volume after processing

    Target: {catalog}.{schema}

    STRICT RULES:
    - ONLY Python code, NO explanations, NO markdown
    - DO NOT use f-strings (use string concatenation)
    - DO NOT create SparkSession
    - Code must be COMPLETE and EXECUTABLE
    """

    attempt = 0
    last_error = None
    code = None

    while attempt < max_retries:
        print(f"\nAttempt {attempt + 1} generating/fixing code...\n")

        # ── On first attempt: generate from scratch ───────────────
        # ── On retry: send failed code + error back to AI ─────────
        if attempt == 0:
            prompt = base_prompt
        else:
            prompt = f"""
            The following PySpark code failed during execution.

            FAILED CODE:
            {code}

            ERROR MESSAGE:
            {last_error}

            Fix the code so it runs successfully.
            Keep the original intent intact.
            Return ONLY corrected Python code. NO explanations. NO markdown.
            """

        code = call_llm(prompt)
        code = code.replace("```python", "").replace("```", "").strip()

        print("===== GENERATED CODE =====\n", code)

        try:
            print("\nExecuting code...\n")
            exec(code, globals())   # ← Run AI-generated code

            print("\n✅ Bronze loading completed!")
            return {
                "status": "success",
                "generated_code": code,
                "attempts": attempt + 1
            }

        except Exception as e:
            last_error = str(e)
            print(f"\n❌ Execution failed (Attempt {attempt + 1})")
            print("Error:", last_error)
            attempt += 1

    print("\n💀 All attempts failed!")
    return {
        "status": "failed",
        "final_code": code,
        "error": last_error,
        "attempts": max_retries
    }
```

**What it does — step by step:**

| Step | What happens |
|------|-------------|
| **Prompt construction** | Builds a precise prompt telling the AI: read CSVs from this Volume path, write to this catalog/schema, follow these exact rules |
| **`call_llm(prompt)`** | Sends prompt to GPT-4o-mini, gets back PySpark code as a string |
| **`exec(code, globals())`** | Runs the AI-generated code in the current Databricks environment |
| **Exception caught** | If `exec()` fails, the error message is captured |
| **Retry prompt** | On retry, the AI receives the failing code AND the error — it reasons about what went wrong and rewrites the fix |
| **Return dict** | Returns `status`, the final generated code, and number of attempts taken |

**Why `exec(code, globals())` instead of `exec(code)`?**
Using `globals()` as the namespace means the generated code has access to `spark`, `dbutils`, and any other objects already defined in the notebook scope. Without this, the AI-generated code can't find the Spark session.

**Why `DO NOT use f-strings` in the prompt?**
F-strings inside a string that you're building with f-strings cause nested brace conflicts (e.g., `f"...{catalog}.{schema}..."` inside another f-string). Instructing the AI to use string concatenation avoids this class of generated-code syntax error completely.

---

### ✅ Cell 4 — Run the Bronze Agent

```python
result = bronze_loader_agent(
    volume_path="/Volumes/env_data/bronze/raw_data/",
    catalog="env_data",
    schema="bronze"
)

print(result)
```

**What happens when you run this:**
1. Agent is called with your Unity Catalog paths
2. AI generates PySpark code to list and ingest all CSVs in the Volume
3. Each CSV becomes a Delta table: `env_data.bronze.<filename>`
4. Files are deleted from the Volume after ingestion (clean inbox pattern)
5. Result dict shows `status: success` and how many attempts it took

**Example output:**
```
Running Bronze Loader Agent...
Volume Path: /Volumes/env_data/bronze/raw_data/

Attempt 1 generating/fixing code...

===== GENERATED CODE =====
files = dbutils.fs.ls("/Volumes/env_data/bronze/raw_data/")
for f in files:
    table_name = f.name.replace(".csv", "").lower()
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(f.path)
    df.write.format("delta").mode("overwrite").saveAsTable("env_data.bronze." + table_name)
    dbutils.fs.rm(f.path)

Executing code...

✅ Bronze loading completed!
{'status': 'success', 'generated_code': '...', 'attempts': 1}
```

---

### ✅ Cell 5 — `silver_cleaning_agent()` — The Intelligent Cleaner

```python
GENERAL_CLEANING_GUIDELINES = """
You are cleaning data from Bronze to Silver.

IMPORTANT:
- Do NOT blindly apply all transformations
- First understand the data
- Then decide what cleaning steps are actually required

Possible cleaning actions (apply ONLY if needed):
- Standardize column names
- Handle null values
- Remove duplicates
- Normalize categorical values

APPROACH:
1. Analyze schema and sample data
2. Create a cleaning plan
3. Generate PySpark code based on that plan
"""

def silver_cleaning_agent(catalog, bronze_schema, silver_schema, user_instructions, max_retries=5):

    print("\n🚀 Running Smart Silver Cleaning Agent...")

    # ── Step 1: Discover all Bronze tables automatically ──────────
    tables = spark.sql(f"SHOW TABLES IN {catalog}.{bronze_schema}") \
                 .select("tableName").collect()
    table_list = [row.tableName for row in tables]
    print("\n📋 Tables found:", table_list)

    results = []

    # ── Step 2: Process each table independently ──────────────────
    for table in table_list:
        print(f"\n🔄 Processing table: {table}")

        # ── Feed real schema and sample data to the AI ────────────
        df = spark.table(f"{catalog}.{bronze_schema}.{table}")
        schema_info = df.dtypes                              # Column names + types
        sample_data = df.limit(5).toPandas().to_dict(orient="records")  # 5 rows

        attempt = 0
        last_error = None
        code = None

        while attempt < max_retries:
            print(f"\n⚙️  Attempt {attempt + 1}...\n")

            if attempt == 0:
                # ── First attempt: full context prompt ────────────
                prompt = f"""
                You are a senior data engineer.

                TABLE: {table}
                SCHEMA: {schema_info}
                SAMPLE DATA: {sample_data}
                USER GUIDELINES: {user_instructions}

                TASK:
                Step 1: Analyze the table
                Step 2: Decide what cleaning is needed (plan internally)
                Step 3: Generate PySpark code to implement ONLY required cleaning

                INPUT:  {catalog}.{bronze_schema}.{table}
                OUTPUT: {catalog}.{silver_schema}.{table}

                IMPORTANT: Apply ONLY necessary transformations. Keep it minimal and safe.

                STRICT RULES:
                - ONLY Python code, NO markdown, NO explanations
                - DO NOT use f-strings
                - DO NOT create SparkSession
                - Code must be COMPLETE and EXECUTABLE
                """
            else:
                # ── Retry: send error back for AI to fix ──────────
                prompt = f"""
                The following PySpark code failed.
                FAILED CODE: {code}
                ERROR: {last_error}
                Fix the code. Return ONLY corrected Python code.
                """

            code = call_llm(prompt)
            code = code.replace("```python", "").replace("```", "").strip()
            if code.lower().startswith("python"):
                code = code[len("python"):].strip()

            print("===== GENERATED CODE =====\n", code)

            try:
                print("\n▶️  Executing...\n")
                exec(code, globals())
                print(f"\n✅ Success: {table}")
                results.append({"table": table, "status": "success", "attempts": attempt + 1})
                break

            except Exception as e:
                last_error = str(e)
                print(f"\n❌ Failed Attempt {attempt + 1} | Error: {last_error}")
                attempt += 1

        if attempt == max_retries:
            results.append({"table": table, "status": "failed", "error": last_error})

    print("\n🏁 All tables processed!")
    return results
```

**What makes this agent "smart" — step by step:**

| Step | Detail |
|------|--------|
| **Auto-discovery** | `SHOW TABLES IN bronze` — the agent finds all tables dynamically, no hardcoding needed |
| **Real schema sent to AI** | `df.dtypes` gives the AI actual column names and types for this specific table |
| **Real sample data sent to AI** | `df.limit(5).toPandas()` gives the AI 5 actual rows — it can see the data format, not just types |
| **AI decides cleaning steps** | The guidelines say "do NOT blindly apply all transformations" — the AI reasons about what THIS table actually needs |
| **Per-table isolation** | Each table has its own retry loop — one failing table doesn't stop others from processing |
| **5 retries** | Silver gets more retries than Bronze (5 vs 3) because cleaning logic is more complex |

**What the AI decides automatically based on sample data:**
- If column names are `UPPER_CASE` → renames to `lower_case`
- If a date column contains `"2024/01/15"` strings → casts to `DateType`
- If a numeric column has `"N/A"` strings → replaces with `null`
- If there are obvious duplicates → adds `dropDuplicates()`
- If a column is perfectly clean → **leaves it alone** (critical — avoids unnecessary changes)

---

### ✅ Cell 6 — Run the Silver Agent

```python
result = silver_cleaning_agent(
    catalog="env_data",
    bronze_schema="bronze",
    silver_schema="silver",
    user_instructions=GENERAL_CLEANING_GUIDELINES
)

print(result)
```

**Example output:**
```
🚀 Running Smart Silver Cleaning Agent...

📋 Tables found: ['customers', 'orders', 'products']

🔄 Processing table: customers
⚙️  Attempt 1...
===== GENERATED CODE =====
from pyspark.sql.functions import col, trim, lower, to_date
df = spark.table("env_data.bronze.customers")
df = df.withColumnRenamed("CustomerID", "customer_id")
df = df.withColumn("email", lower(trim(col("Email"))))
df = df.withColumn("signup_date", to_date(col("SignupDate"), "yyyy/MM/dd"))
df = df.dropDuplicates(["customer_id"])
df.write.format("delta").mode("overwrite").saveAsTable("env_data.silver.customers")

▶️  Executing...
✅ Success: customers

🔄 Processing table: orders
...

🏁 All tables processed!
[
  {'table': 'customers', 'status': 'success', 'attempts': 1},
  {'table': 'orders',    'status': 'success', 'attempts': 2},
  {'table': 'products',  'status': 'success', 'attempts': 1}
]
```

---

## 🔄 Self-Healing Flow Visualised

```
bronze_loader_agent() called
         │
         ▼
   Build base prompt
         │
         ▼
   call_llm(prompt)  ──────────────────────────► Azure OpenAI GPT-4o-mini
         │                                              │
         ◄──────────────────────────────── PySpark code string
         │
         ▼
   exec(code, globals())
         │
    ┌────┴──────────┐
    │               │
  SUCCESS        EXCEPTION
    │               │
    ▼               ▼
  Return        Capture error
  result        Build retry prompt:
                  "Here is the code: ...
                   Here is the error: ...
                   Fix it."
                     │
                     ▼
               call_llm(retry_prompt)
                     │
                     ▼
               exec(fixed_code)
                     │
               (repeats up to max_retries)
```

---

## 💡 What's Good About This Code

| Design Choice | Why It's Smart |
|---------------|---------------|
| **No hardcoded schema** | Works for ANY CSV — the agent reads whatever arrives |
| **No hardcoded cleaning rules** | AI adapts cleaning per table based on actual data |
| **Error → retry loop** | Runtime errors become prompts. AI rewrites its own mistakes |
| **`exec(code, globals())`** | Generated code accesses `spark` and `dbutils` without re-declaring them |
| **`DO NOT use f-strings` rule** | Prevents brace-conflict syntax errors in generated code |
| **5-row sample to AI** | Gives AI real data context, not just abstract types |
| **Per-table results dict** | Clear audit trail — which tables succeeded, which failed, how many attempts |

---

## 🚧 What to Add Next (Gold Layer)

This notebook covers Bronze and Silver. The next notebook to build:

```python
# Notebook 2: gold_aggregation_agent.py

def gold_aggregation_agent(catalog, silver_schema, gold_schema, business_rules):
    """
    AI agent that reads Silver tables and generates
    business aggregation code (KPIs, joins, rollups).
    Writes to Gold Delta tables for reporting.
    """
    # ... same agentic pattern as Silver agent
```

---

## ⚙️ How to Add to Your Repository

This notebook maps to these files in the repo:

```
self-healing-agentic-pipeline/
├── notebooks/
│   └── 01_bronze_silver_agent.py     ← Export from Databricks as Source File
│
├── src/
│   ├── agents/
│   │   ├── bronze_loader_agent.py    ← Refactored as importable module
│   │   └── silver_cleaning_agent.py
│   └── utils/
│       └── llm_client.py             ← call_llm() as shared utility
│
└── configs/
    └── pipeline_config.yaml          ← Volume paths, catalog, schema names
```

### Export from Databricks

1. Open notebook in Databricks
2. **File → Export → Source File (.py)**
3. Place the `.py` file in `notebooks/` folder
4. Commit to GitHub — it renders cleanly as code

### pipeline_config.yaml (put non-secret config here)

```yaml
# configs/pipeline_config.yaml
bronze:
  catalog: env_data
  schema: bronze
  volume_path: /Volumes/env_data/bronze/raw_data/

silver:
  catalog: env_data
  schema: silver

openai:
  api_version: "2024-12-01-preview"
  deployment: gpt-4o-mini
  # endpoint stored in Databricks secret scope
```

---

## 🎤 How to Explain This in an Interview

**"What does the Bronze agent actually do?"**
> "It receives a Volume path and catalog target. Instead of me writing a for-loop to ingest CSVs, I give that task to GPT-4o-mini. The AI writes the PySpark code, I exec() it. If it fails — maybe the file path format was different — the error goes back to the AI with the failed code, and it rewrites a fix. So ingestion of any CSV into Delta is completely automated."

**"How does the Silver agent know what cleaning to apply?"**
> "It feeds the actual schema and five rows of real data to the AI for each table. The AI sees, for example, that a 'signup_date' column has values like '2024/01/15' as strings, and it generates a to_date() cast. Or it sees email addresses in mixed case and lowercases them. It makes data-driven decisions per table — not a one-size-fits-all cleaning script."

**"Isn't exec() dangerous?"**
> "There's a real tradeoff. In a controlled Databricks environment with proper RBAC, it's acceptable. The generated code only has access to what's already in the notebook scope — spark and dbutils. For production hardening, I'd add a code review step where the generated code is logged and optionally reviewed before exec, and I'd validate that it only calls known safe PySpark functions."

**"Why gpt-4o-mini instead of GPT-4?"**
> "Cost and speed. This model is called on every retry, and in a pipeline processing 20 tables with up to 5 retries each, that's potentially 100 API calls. GPT-4o-mini handles structured code generation reliably at a fraction of the cost, and the prompt engineering compensates for any capability gap."

---

*Part of the [Self-Healing Agentic Data Pipeline](../README.md) portfolio project.*
