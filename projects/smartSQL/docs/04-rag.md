# RAG — Retrieval-Augmented Generation

[← LangChain Pipeline](./03-langchain.md) · [Data Layer →](./05-data-layer.md)

---

## The problem RAG solves

GPT-4o-mini was trained on general internet text. It knows SQL syntax well. But it has no knowledge of your specific:

- Table names (`landings`, `taxi_trips`, `nfis_catch`)
- Column names (`tpep_pickup_datetime`, `gear_type`, `vessel_id`)
- Query patterns that work correctly against your schema
- Business rules encoded in your data

Without RAG, the model guesses — and frequently produces syntactically valid SQL that references the wrong column names or uses the wrong aggregation logic.

**RAG solves this by giving the model examples.** Before answering, the system retrieves the five SQL patterns most similar to the user's question and provides them as context. The model adapts a proven example rather than guessing from scratch.

---

## How RAG works in SmartSQL

```
User question
      │
      ▼
text-embedding-ada-002
      │  converts question to 1,536-dim vector
      ▼
Azure AI Search index
      │  hybrid search: vector + keyword
      │  returns 5 most similar SQL patterns
      ▼
GPT-4o-mini prompt
      │  system prompt + schema + 5 examples + question
      ▼
Generated SQL (adapted from examples)
```

---

## The Azure AI Search index

### What is stored — SQL patterns, not data

The index contains pre-written SQL query patterns that are known to work against your schema. For example:

```sql
-- Pattern: total by category and time period
SELECT gear_type, YEAR(landing_date) AS year,
       SUM(catch_kg) AS total_catch
FROM landings
WHERE YEAR(landing_date) = {year}
GROUP BY gear_type, YEAR(landing_date)
ORDER BY total_catch DESC

-- Pattern: count records with filter
SELECT COUNT(*) AS total_records
FROM landings
WHERE site_name LIKE '%{site}%'
  AND quarter = {quarter}

-- Pattern: average by group
SELECT vessel_type, AVG(catch_kg) AS avg_catch
FROM landings
GROUP BY vessel_type
ORDER BY avg_catch DESC
```

These patterns are indexed — vectorised into embeddings and stored in Azure AI Search. **No actual catch data, vessel data, or personally identifiable information is in the index.**

### Why this is the key security design decision

Because the index contains only SQL patterns:
- No sensitive data is exposed if the Azure AI Search index is compromised
- No data sovereignty or regulatory issues with sending queries to Azure
- The system works even if the underlying database changes or is moved

---

## text-embedding-ada-002

The embedding model converts text to a numerical vector — a list of 1,536 floating-point numbers that captures the semantic meaning of the text.

Two questions with the same meaning but different words will have vectors close together in this 1,536-dimensional space:

```
"show total catch by gear"     → [0.23, -0.11, 0.87, ...]
"display aggregate by gear"    → [0.24, -0.10, 0.85, ...]  (similar!)

"total catch by gear"          → similar to both above
"quarterly revenue by product" → very different vector
```

This is why semantic search finds relevant patterns even when the user's wording differs from the indexed patterns.

**Deployment name:** `text-embedding-ada-002`  
**Vector dimensions:** 1,536  
**API version:** `2023-05-15`

### The correct `embedding_dependency` format

The most common configuration mistake is passing the full embeddings URL in `extra_body`. Azure expects the deployment name only when the embedding model is in the same resource as the chat model:

```python
# WRONG — causes "Invalid embedding endpoint" error
"embedding_dependency": {
    "type": "endpoint",
    "endpoint": "https://myresource.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"
}

# CORRECT — same resource as chat model
"embedding_dependency": {
    "type": "deployment_name",
    "deployment_name": "text-embedding-ada-002"
}
```

---

## Hybrid search

SmartSQL uses `query_type: "vector_simple_hybrid"` — combining two search methods:

| Method | How it works | Strength |
|--------|-------------|----------|
| **Vector search** | Finds patterns with similar meaning | Works with different vocabulary |
| **Keyword search** | Finds patterns with matching words | Precise on exact column names |
| **Hybrid (combined)** | Merges both rankings | Best of both worlds |

### Why hybrid matters

A user asks: *"average fare per zone"*

- **Vector search** finds patterns about averages and grouping — semantically similar
- **Keyword search** finds patterns containing "fare" — exact match on the business term
- **Hybrid** returns patterns that are both semantically similar AND contain the right field names

---

## RAG configuration in `extra_body`

```python
_RAG_EXTRA_BODY = {
    "data_sources": [{
        "type": "azure_search",
        "parameters": {
            "endpoint":   SEARCH_ENDPOINT,      # Azure AI Search URL
            "index_name": SEARCH_INDEX,          # your SQL patterns index
            "authentication": {
                "type": "api_key",
                "key":  SEARCH_KEY
            },
            "embedding_dependency": {
                "type":            "deployment_name",
                "deployment_name": "text-embedding-ada-002"
            },
            "query_type":      "vector_simple_hybrid",
            "in_scope":        True,   # only return results from the index
            "strictness":      3,      # 1-5: relevance filtering strength
            "top_n_documents": 5,      # return 5 most similar patterns
        },
    }]
}

LLM = AzureChatOpenAI(...).bind(extra_body=_RAG_EXTRA_BODY)
```

**Strictness 3:** Balanced between returning enough context and filtering out irrelevant patterns. At strictness 5, only very close matches are returned — good for narrow domains. At strictness 1, many patterns are returned — useful for broad exploratory queries.

---

## What goes into the LLM prompt

The final prompt sent to GPT-4o-mini looks like this (simplified):

```
SYSTEM:
You are an AI assistant for SQL generation.

Table: landings
Columns: gear_type (VARCHAR), catch_kg (FLOAT), landing_date (DATE), site_name (VARCHAR)

Rules: SELECT only. Use LIKE for strings. Return SQL only.

Retrieved SQL patterns (use as reference):
[Pattern 1]: SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type
[Pattern 2]: SELECT site_name, COUNT(*) FROM landings WHERE YEAR(landing_date) = 2025
...

USER:
show total catch by boat gear for Q2 2025
```

The model reads the patterns, sees how your schema is structured, and adapts the most relevant example to answer the specific question.

---

## When RAG is not configured

If `SEARCH_ENDPOINT` and `SEARCH_KEY` are left blank in `.env`, the system falls back gracefully to schema-only mode. The LLM still receives:

- The table name and all column names/types (from `get_schema()`)
- The full system prompt with SQL rules
- The user's question

This works well for simple queries. RAG significantly improves accuracy for complex multi-table queries, time-period filters, and domain-specific terminology.

---

## Building your own SQL pattern index

### Step 1 — Collect good queries

Start with 20–50 SQL queries you know are correct for your schema. Focus on the most common question types your users ask.

### Step 2 — Create the Azure AI Search index

In Azure Portal → AI Search → create an index with fields:
- `id` (Edm.String, key)
- `content` (Edm.String, searchable) — the SQL query text
- `description` (Edm.String, searchable) — natural language description
- `content_vector` (Collection(Edm.Single), searchable, dimensions: 1536)

### Step 3 — Index your patterns

```python
import duckdb, json
from openai import AzureOpenAI
from azure.search.documents import SearchClient

client = AzureOpenAI(...)
search = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME, ...)

for i, pattern in enumerate(sql_patterns):
    embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=pattern["description"]
    ).data[0].embedding

    search.upload_documents([{
        "id": str(i),
        "content": pattern["sql"],
        "description": pattern["description"],
        "content_vector": embedding
    }])
```

### Step 4 — Maintain the index

Re-index when the schema changes (new columns, renamed tables). Automate this as a CI/CD step triggered by schema migrations.

---

[← LangChain Pipeline](./03-langchain.md) · [Data Layer →](./05-data-layer.md)
