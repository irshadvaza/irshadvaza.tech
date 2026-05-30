# Architecture

[← Back to README](../README.md) · [Security Model →](./02-security.md)

---

![Smart SQL Architecture](assets/images/smart-sql-architecture.png)


## System overview

SmartSQL is structured in four distinct zones. The boundary between Zone 3 (Azure cloud) and Zone 4 (local execution) is the critical security boundary — raw data never crosses it.

```
┌─────────────────────────────────────────────────────────────┐
│  ZONE 1 — User Interface (Streamlit)                        │
│                                                             │
│   [Speech input]      [Text input]      [Results display]  │
│   Google STT          500 char max      Table + Chart + CSV │
└──────────────┬─────────────┬────────────────────────────────┘
               │             │
               └──────┬──────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  ZONE 2 — Security Gate                                     │
│                                                             │
│   Rate limit (10/60s) → Input validation → Content Safety  │
└─────────────────────────┬───────────────────────────────────┘
                          │  clean question text only
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ZONE 3 — Azure Cloud (AI Foundry)              ☁           │
│                                                             │
│   ┌──────────────────────────────────────────┐             │
│   │  RAG pipeline                            │             │
│   │  Question → text-embedding-ada-002       │             │
│   │           → Azure AI Search (SQL index)  │             │
│   │           → 5 similar SQL patterns       │             │
│   └──────────────┬───────────────────────────┘             │
│                  │ patterns + question                      │
│                  ▼                                          │
│          GPT-4o-mini (Azure AI Foundry)                     │
│                  │                                          │
│                  │  SQL text only ◄── no data crosses up    │
└──────────────────┼──────────────────────────────────────────┘
                   │  generated SQL script only
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  ZONE 4 — Local / Private Environment          🔒           │
│                                                             │
│   SQL validation → DuckDB / Azure SQL → Audit log          │
│   (SELECT only)    (read-only conn)     (hashed)            │
│                          │                                  │
│                          ▼                                  │
│                    DataFrame results                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                    Back to Zone 1 UI
```

---

## Component responsibilities

### Streamlit UI (`mainui.py`)

- Accepts text input (max 500 characters enforced at UI level)
- Accepts speech input via Google Speech-to-Text integration
- Manages session state: stores last query, SQL output, and result DataFrame
- Rate limit display in sidebar (queries remaining per 60s window)
- Schema browser sidebar: shows all column names and types from the data source
- Renders results table, interactive chart panel (Bar / Line / Pie), and CSV download
- Shows row-cap warning when results exceed 5,000 rows

### Security gate (`llm_langchain.py` — validate steps)

- **Rate limiter**: token bucket per Streamlit session; 10 requests per 60 seconds
- **Input validator**: strips whitespace, checks length, matches 12 blocked regex patterns
- **Content Safety**: calls Azure Content Safety API; four harm categories; severity threshold 2

### LangChain LCEL chain (`llm_langchain.py`)

```python
_CHAIN = (
    RunnableLambda(validate_input)
    | RunnableLambda(check_content_safety)
    | PROMPT                                # ChatPromptTemplate
    | LLM                                   # AzureChatOpenAI + .bind(extra_body=RAG)
    | StrOutputParser()
    | RunnableLambda(clean_sql_output)
)
```

Each step is independently testable. Swapping the LLM (GPT-4o-mini → Claude → Gemini) is one line.

### Azure AI Search + Embeddings (RAG)

- Index contains pre-written SQL query patterns — **not raw data**
- `text-embedding-ada-002` vectorises the user question into 1,536 dimensions
- Hybrid search: vector similarity + keyword matching (`vector_simple_hybrid`)
- Returns 5 most similar patterns as context for the LLM
- Strictness: 3 (balanced relevance filtering)

### GPT-4o-mini (Azure AI Foundry)

- Receives: system prompt with schema + SQL rules + 5 RAG examples + user question
- Returns: raw SQL text only
- Temperature: 0.3 (deterministic, not creative)
- API version: `2024-02-15-preview`

### SQL validation + execution (`db_handler.py` / `db_handler_parquet.py`)

- Validates SQL starts with SELECT; blocks 12 dangerous keywords
- Executes via SQLAlchemy (Azure SQL) or DuckDB (parquet)
- Read-only connection intent (`ApplicationIntent=ReadOnly`)
- Row cap: 5,000 rows maximum
- Audit log: SHA-256 hash, duration (ms), row count, success flag

---

## Data flow — step by step

| Step | What happens | Where |
|------|-------------|-------|
| 1 | User types or speaks a question | Local browser |
| 2 | Speech converted to text (if applicable) | Google Cloud |
| 3 | Rate limit checked | Local session state |
| 4 | Input sanitised and validated | Local — `validate_input()` |
| 5 | Content Safety screening | Azure Content Safety API |
| 6 | Question formatted into chat messages | Local — `ChatPromptTemplate` |
| 7 | Question vectorised | Azure OpenAI (ada-002) |
| 8 | Similar SQL patterns retrieved | Azure AI Search |
| 9 | SQL generated by LLM | Azure OpenAI (GPT-4o-mini) |
| 10 | SQL validated (SELECT only, no DDL) | Local — `clean_sql_output()` |
| 11 | SQL executed against database | Local — DuckDB or Azure SQL |
| 12 | Results capped, audit log written | Local |
| 13 | Results rendered in Streamlit | Local browser |

---

## LangGraph version (v2)

The LangGraph version adds an automatic retry loop. When generated SQL fails to execute, the agent routes back to the Generate node with the error message attached to the shared state. The LLM sees its previous failed SQL and the exact error, corrects it, and retries — silently, without the user seeing an error.

```
validate ──► generate ──► execute ──► [success] END
                ▲              │
                │   bad SQL    │
                └──────────────┘  (up to 3 retries)
```

See [`llm_langgraph.py`](../llm_langgraph.py) for the full implementation.

---

[← Back to README](../README.md) · [Security Model →](./02-security.md)
