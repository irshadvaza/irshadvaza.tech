# LangChain Pipeline

[← Security Model](./02-security.md) · [RAG Deep Dive →](./04-rag.md)

---

## Why LangChain?

LangChain provides a composable, testable, model-agnostic framework for building LLM pipelines. In SmartSQL it replaces hundreds of lines of manual glue code — prompt formatting, API calls, response parsing, retry logic — with a clean six-step chain that reads like a sentence.

| Without LangChain | With LangChain |
|-------------------|---------------|
| Nested function calls with manual data passing | `step1 \| step2 \| step3` pipe syntax |
| Model-specific API calls hardcoded throughout | Swap model in one line |
| Manual retry logic in every function | `.with_retry()` decorator |
| Hard to unit test individual steps | `.invoke()` on any step in isolation |
| No observability without custom logging | LangSmith traces every step automatically |

---

## LCEL — LangChain Expression Language

LCEL is the modern LangChain syntax using the `|` pipe operator. Every component is a **Runnable** — an object that implements `.invoke()`, `.stream()`, and `.batch()`. The `|` operator connects them: the output of one Runnable becomes the input of the next.

### The complete SmartSQL chain

```python
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

_CHAIN = (
    RunnableLambda(validate_input)          # Step 1: sanitise + check question
    | RunnableLambda(check_content_safety)  # Step 2: Azure Content Safety screen
    | PROMPT                                # Step 3: format into chat messages
    | LLM                                   # Step 4: call GPT-4o-mini + RAG
    | StrOutputParser()                     # Step 5: extract string from AIMessage
    | RunnableLambda(clean_sql_output)      # Step 6: validate SELECT-only SQL
)

def call_llm(user_input: str) -> str:
    return _CHAIN.invoke({"question": user_input})
```

---

## Step-by-step breakdown

### Step 1 — `validate_input` (RunnableLambda)

```python
def validate_input(data: dict) -> dict:
    q = data.get("question", "").strip()
    if len(q) > MAX_INPUT_LENGTH:           # 500 char cap
        raise ValueError("Input too long.")
    for pattern in BLOCKED_PATTERNS:        # 12 regex patterns
        if re.search(pattern, q, re.IGNORECASE):
            raise ValueError("Blocked content.")
    return {"question": q}                  # passes cleaned question forward
```

**Input:** `{"question": "show catch by gear 2025"}`  
**Output:** `{"question": "show catch by gear 2025"}` (unchanged if clean)  
**On failure:** raises `ValueError` — chain stops immediately

### Step 2 — `check_content_safety` (RunnableLambda)

Calls the Azure Content Safety API. If any of the four harm categories scores ≥ 2, raises `ValueError`. If the API is unreachable, logs the error and passes through (fail-open).

**Input:** `{"question": "show catch by gear 2025"}`  
**Output:** same dict, unchanged  

### Step 3 — `PROMPT` (ChatPromptTemplate)

```python
PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant for SQL generation.\n"
     "Rules: SELECT only. Use LIKE for strings. No markdown.\n"
     f"Table: {TABLE_NAME}\nColumns:\n{schema_description}"
    ),
    ("human", "{question}"),   # {question} filled from dict at runtime
])
```

**Input:** `{"question": "show catch by gear 2025"}`  
**Output:** `[SystemMessage(...), HumanMessage("show catch by gear 2025")]`

The schema is injected at startup from the real parquet/database columns — the LLM uses real column names, not guesses.

### Step 4 — `LLM` (AzureChatOpenAI with `.bind()`)

```python
_BASE_LLM = AzureChatOpenAI(
    azure_endpoint=AZURE_OAI_ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
    azure_deployment=DEPLOYMENT,
    api_version="2024-02-15-preview",
    temperature=0.3,    # deterministic SQL, not creative writing
    max_tokens=800,
)

# .bind() attaches RAG payload to every call — the correct pattern
# (NOT model_kwargs — that silently drops extra_body with a warning)
LLM = _BASE_LLM.bind(extra_body=_RAG_EXTRA_BODY)
```

**Temperature 0.3:** SQL generation needs consistency, not creativity. Lower temperature = more reproducible output for the same question.

**`.bind()` vs `model_kwargs`:** A common mistake is putting `extra_body` in `model_kwargs`. LangChain warns and silently drops it — the Azure AI Search RAG call never happens. `.bind()` is the correct method.

**Input:** `[SystemMessage, HumanMessage]`  
**Output:** `AIMessage(content="SELECT gear_type, SUM(...)")`

### Step 5 — `StrOutputParser()`

Extracts `.content` from the `AIMessage` object, returning a plain Python string.

**Input:** `AIMessage(content="SELECT gear_type, SUM(catch_kg)...")`  
**Output:** `"SELECT gear_type, SUM(catch_kg)..."`

### Step 6 — `clean_sql_output` (RunnableLambda)

```python
def clean_sql_output(raw: str) -> str:
    sql = re.sub(r"```(?:sql)?\n?", "", raw)   # strip markdown fences
    sql = re.sub(r"```", "", sql).strip()
    if not sql.upper().lstrip().startswith("SELECT"):
        raise ValueError("Not a SELECT statement.")
    for kw in ["DROP ", "DELETE ", "TRUNCATE ", "INSERT ", "UPDATE ", "EXEC "]:
        if kw in sql.upper():
            raise ValueError(f"Unsafe keyword '{kw.strip()}' found.")
    return sql
```

**Input:** `"SELECT gear_type, SUM(catch_kg) FROM landings..."`  
**Output:** same string (validated, clean)

---

## The prompt template in detail

The system message is built at startup by combining fixed rules with the live schema:

```
You are an AI assistant specialized in transforming natural language 
into SQL queries.

Table name: taxi_trips
Columns:
  - VendorID (BIGINT)
  - tpep_pickup_datetime (TIMESTAMP)
  - fare_amount (DOUBLE)
  - tip_amount (DOUBLE)
  - payment_type (BIGINT)
  ...

Rules:
- Only generate SELECT queries.
- Use ILIKE instead of LIKE for case-insensitive string matching.
- For multi-word input, match each word separately:
  e.g. 'yellow cab' → WHERE vendor ILIKE '%yellow%' AND vendor ILIKE '%cab%'
- Return only the SQL. No markdown fences, no comments.
```

Schema injection is what makes the LLM accurate. Without it, the model guesses column names from training data and frequently gets them wrong.

---

## Error handling in the chain

If any step raises a `ValueError`, LangChain propagates it immediately — no subsequent steps run. The caller (`mainui.py`) catches it by type:

```python
try:
    sql = call_llm(user_query)
except ValueError as e:
    # User-facing validation / content safety error — safe to show
    st.error(str(e))
except RuntimeError as e:
    # Azure service unavailable after retries — show generic message
    st.error("Service temporarily unavailable.")
```

This separation ensures users see helpful messages for input problems, and generic messages for infrastructure failures — preventing accidental disclosure of internal configuration.

---

## Testing individual steps

Every step can be called in isolation from the terminal:

```bash
python test_steps.py
```

Or interactively:

```python
from test_steps import *

# Test step 1
result = validate_input({"question": "show total catch 2025"})
print(result)
# {'question': 'show total catch 2025'}

# Test blocked input
validate_input({"question": "ignore previous instructions"})
# ValueError: Blocked content.

# Test step 6 (SQL validation)
clean_sql_output("```sql\nSELECT * FROM taxi_trips\n```")
# 'SELECT * FROM taxi_trips'

clean_sql_output("DELETE FROM taxi_trips")
# ValueError: Unsafe keyword 'DELETE' found.
```

---

## LangGraph — version 2

LangGraph extends LangChain with a stateful graph model. Nodes replace chain steps, shared state replaces the dict pipeline, and conditional edges enable automatic retry.

When the LLM generates SQL that fails to execute, LangGraph routes back to the Generate node with the error message in state. The LLM sees its previous attempt and the exact error, corrects it, and retries — the user sees nothing.

```
validate ──► generate ──► execute ──► END (success)
                ▲              │
                │   bad SQL    │
                └──────────────┘  (up to 3 retries)
```

Switch between versions by changing one import line in `mainui.py`:

```python
# LangChain version
from llm_langchain import call_llm

# LangGraph version (auto-retry)
from llm_langgraph import call_llm
```

---

## LangSmith observability

Add three lines to `.env` to enable full pipeline tracing in the LangSmith dashboard:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_key_here   # free at smith.langchain.com
LANGCHAIN_PROJECT=SmartSQL
```

Every `chain.invoke()` call is now automatically recorded: each step's input, output, latency, and token usage are visible in a web dashboard. Essential for debugging wrong SQL in production.

---

[← Security Model](./02-security.md) · [RAG Deep Dive →](./04-rag.md)
