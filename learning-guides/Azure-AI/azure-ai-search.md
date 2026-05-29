# Azure AI Search — Complete Guide

> **Learning Guide** · Azure AI Series · Part 1 of 8  
> Author: Irshad Vaza · AI & Data Specialist · [irshadvaza.tech](https://irshadvaza.tech)  
> Last updated: 2025

[![Azure](https://img.shields.io/badge/Azure-AI_Search-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/en-us/products/ai-services/ai-search)
[![Level](https://img.shields.io/badge/Level-Beginner_to_Expert-brightgreen)](.)
[![Real Project](https://img.shields.io/badge/Used_in-SmartSQL_Project-purple)](../projects/smartSQL.md)

---

## Table of Contents

1. [What is Azure AI Search?](#1-what-is-azure-ai-search)
2. [Real-world analogy](#2-real-world-analogy)
3. [How it fits in an AI system](#3-how-it-fits-in-an-ai-system)
4. [Core search components](#4-core-search-components)
   - [Data Source](#41-data-source)
   - [Indexer](#42-indexer--the-engine)
   - [Skillset](#43-skillset--the-ai-brain)
   - [Index](#44-index--the-library-catalogue)
   - [Search Application](#45-search-application--the-user-facing-layer)
5. [Index vs Indexer vs Indexing — explained](#5-index-vs-indexer-vs-indexing--the-three-words-that-confuse-everyone)
6. [Pricing tiers](#6-pricing-tiers)
7. [Capacity management — Replicas, Partitions, Search Units](#7-capacity-management)
8. [Search types](#8-search-types)
9. [Used in SmartSQL](#9-how-i-used-it-in-smartsql)
10. [Interview Q&A](#10-interview-qa)
11. [What to learn next](#11-what-to-learn-next)

---

## 1. What is Azure AI Search?

**Simple answer:** Azure AI Search is Microsoft's managed cloud search engine. You give it your data, it makes that data searchable — using keywords, meaning, or both at the same time.

**Technical answer:** Azure AI Search is a fully managed search-as-a-service platform on Azure that provides:

- **Full-text search** — find documents containing specific words
- **Semantic search** — find documents by meaning, not just exact words
- **Vector search** — find documents by mathematical similarity (used in AI / RAG)
- **Hybrid search** — combine all three for best results
- **AI enrichment** — extract insights from your data automatically during indexing (OCR, language detection, entity recognition, key phrases)

> **In SmartSQL:** Azure AI Search stores SQL query patterns as vectors. When a user types a question, the search finds the 5 most similar SQL patterns and sends them to GPT-4o-mini as examples. This is called RAG (Retrieval-Augmented Generation).

---

## 2. Real-world analogy

Think of Azure AI Search like a **university library system**.

| Library concept | Azure AI Search concept |
|----------------|------------------------|
| Books and journals | Your raw data (PDFs, SQL rows, blobs) |
| Librarian cataloguing books | The **Indexer** (reads and processes your data) |
| AI assistant tagging each book | The **Skillset** (extracts topics, entities, keywords) |
| The card catalogue | The **Index** (searchable version of your data) |
| A student searching the catalogue | The **Search application** (your code calling the API) |
| Finding books on "climate" even if they use "environment" | **Semantic / Vector search** |

The key idea: **you don't search your raw data**. The indexer reads your raw data, processes and enriches it, then stores a searchable version in the index. You search the index — which is fast, structured, and AI-enhanced.

---

## 3. How it fits in an AI system

```
Your raw data                    Azure AI Search service
(Blob Storage,    ──────────►   ┌─────────────────────────────┐
 SQL Database,      Indexer     │  Index (searchable version)  │
 Cosmos DB,         runs        │  with vectors + metadata     │
 SharePoint...)                 └─────────────┬───────────────┘
                                              │
                                    User asks a question
                                              │
                                    Question vectorised
                                    (text-embedding-ada-002)
                                              │
                                    Similar documents found
                                    (Top 5 by similarity)
                                              │
                                    ┌─────────▼──────────┐
                                    │   LLM (GPT-4o-mini) │
                                    │ question + examples │
                                    │ → generates answer  │
                                    └────────────────────┘
```

This pattern is called **RAG — Retrieval-Augmented Generation**.  
Azure AI Search is the "R" — the Retrieval part.

---

## 4. Core search components

Azure AI Search has four core components: a data source, a skillset, an index, and an indexer. The indexer extracts documents from the data source, applies the skillset, and populates the index.

Here is the complete flow with a real example. Imagine you are building a search system for a fisheries agency's documents — annual reports, research papers, and regulation PDFs stored in Azure Blob Storage.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DATA SOURCE │───►│   INDEXER    │───►│   SKILLSET   │───►│    INDEX     │
│              │    │              │    │  (optional   │    │              │
│ Azure Blob   │    │ Reads files  │    │   AI magic)  │    │ Searchable   │
│ Azure SQL    │    │ Cracks docs  │    │              │    │ structured   │
│ Cosmos DB    │    │ Extracts text│    │ OCR, NER,    │    │ data with    │
│ SharePoint   │    │ Schedules    │    │ Key phrases  │    │ vectors      │
│              │    │ auto-runs    │    │ Translation  │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                    │
                                                                    ▼
                                                          ┌──────────────────┐
                                                          │ SEARCH           │
                                                          │ APPLICATION      │
                                                          │ (your code,      │
                                                          │  SmartSQL,       │
                                                          │  chatbot, etc.)  │
                                                          └──────────────────┘
```

---

### 4.1 Data Source

**What it is:** A connection definition telling Azure AI Search where your raw data lives.

**Supported sources include:**
- Azure Blob Storage (PDFs, Word, HTML, JSON, CSV, images)
- Azure SQL Database
- Azure Cosmos DB
- Azure Table Storage
- Azure Data Lake Storage Gen2
- SharePoint Online
- OneLake (Microsoft Fabric)

**Real example — fisheries agency:**
```json
{
  "name": "fisheries-documents",
  "type": "azureblob",
  "credentials": {
    "connectionString": "DefaultEndpointsProtocol=https;AccountName=..."
  },
  "container": {
    "name": "annual-reports"
  }
}
```

**Simple explanation:** This is just the address. "My data is in this Azure Blob Storage container." Azure AI Search connects to it when the indexer runs.

---

### 4.2 Indexer — The Engine

**What it is:** The worker that does the actual work. It reads from the data source, optionally passes content through the skillset, and writes the results into the index.

**Simple analogy:** If the data source is a warehouse of boxes (raw documents), the indexer is the forklift driver who opens each box, reads what is inside, and puts each item on the right shelf in the library.

**What the indexer does step by step:**

```
Step 1: DOCUMENT CRACKING
  Opens each file (PDF, Word, HTML, image...)
  Extracts raw text and images
  Even handles encrypted or password-protected files

Step 2: FIELD MAPPING
  Maps raw fields to your index schema
  e.g. file metadata "author" → index field "document_author"

Step 3: SKILLSET EXECUTION (if skillset attached)
  Sends content through each AI skill
  OCR on images → extracted text
  Entity recognition → "EAD", "Irshad Vaza" → named entities stored

Step 4: INDEX POPULATION
  Writes enriched content into the index
  Generates vectors (if embedding skill configured)
  Marks document as indexed with a watermark/timestamp

Step 5: CHANGE DETECTION (on scheduled runs)
  Checks what changed since the last run
  Only re-indexes modified or new documents
  Skips unchanged documents → saves time and cost
```

**Indexer scheduling:**
```json
{
  "name": "fisheries-indexer",
  "dataSourceName": "fisheries-documents",
  "targetIndexName": "fisheries-index",
  "skillsetName": "fisheries-skillset",
  "schedule": {
    "interval": "PT2H",
    "startTime": "2025-01-01T00:00:00Z"
  }
}
```
`PT2H` = run every 2 hours. Supports: `PT5M` (5 min), `PT1H` (1 hour), `P1D` (1 day).

> **In SmartSQL:** There is no indexer running on a schedule because the SQL pattern index is populated manually — it is a one-time setup of curated examples, not a live data stream. If the schema changes, the index is manually re-populated.

---

### 4.3 Skillset — The AI Brain

**What it is:** An optional set of AI-powered processing steps that enrich your content before it is indexed. A skillset specifies atomic enrichment steps. Enrichment starts when the indexer cracks documents and extracts images and text. The type of processing that occurs next depends on your data and the skills you have added to a skillset.

**Simple analogy:** Imagine you receive a box of books in a foreign language with no table of contents. The skillset is the specialist team that: translates the text, reads the images, highlights key topics, finds all the people and organisations mentioned, and writes a summary — before the librarian catalogues the book.

**Built-in skills (no custom code needed):**

| Skill | What it does | Example |
|-------|-------------|---------|
| OCR (Optical Character Recognition) | Reads text from images and scanned PDFs | Scanned fishing licence PDF → searchable text |
| Language Detection | Detects which language the document is in | "This is Arabic" |
| Text Translation | Translates to English (or any language) | Arabic report → English |
| Entity Recognition | Finds people, organisations, locations, dates | "EAD", "Abu Dhabi", "2025-03-15" |
| Key Phrase Extraction | Finds the most important phrases | "boat gear", "catch quota", "Q2 2025" |
| Sentiment Analysis | Positive / negative / neutral | Compliance report is "negative" sentiment |
| Image Analysis | Describes what is in a photo | "Fishing vessel, morning, harbour" |
| Text Split | Chunks large documents into smaller pieces | 50-page PDF → 100 chunks of 512 tokens |
| **Text Embedding** | Converts text to a vector (for semantic search) | "catch by gear" → [0.23, -0.11, 0.87...] |

**Custom skills:** Custom skills allow you to integrate your own code or models. Classification models that identify salient characteristics of various document types fall into this category, but any external package that adds value to your content could be used.

**Real skillset example — fisheries document enrichment:**
```json
{
  "name": "fisheries-skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
      "name": "ocr-skill",
      "inputs":  [{"name": "image", "source": "/document/normalized_images/*"}],
      "outputs": [{"name": "text",  "targetName": "ocr_text"}]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.EntityRecognitionSkill",
      "name": "entity-skill",
      "categories": ["Organization", "Person", "Location", "DateTime"],
      "inputs":  [{"name": "text", "source": "/document/content"}],
      "outputs": [{"name": "organizations", "targetName": "organizations"},
                  {"name": "locations",     "targetName": "locations"}]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
      "name": "keyphrases-skill",
      "inputs":  [{"name": "text", "source": "/document/content"}],
      "outputs": [{"name": "keyPhrases", "targetName": "key_phrases"}]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "embedding-skill",
      "resourceUri": "https://my-resource.openai.azure.com",
      "deploymentId": "text-embedding-ada-002",
      "inputs":  [{"name": "text", "source": "/document/content"}],
      "outputs": [{"name": "embedding", "targetName": "content_vector"}]
    }
  ]
}
```

If an indexer is a pipeline, you can think of a skillset as a "pipeline within the pipeline." The output of a skillset is manifested internally as a tree structure referred to as an enriched document.

---

### 4.4 Index — The Library Catalogue

**What it is:** The searchable, structured store of your enriched content. Not the raw data — the processed, queryable version.

**Simple analogy:** The index is like the library's card catalogue. Each card represents one document and contains all the information you need to find it (title, author, keywords, summary). The actual books stay on the shelves (your original storage). The catalogue is what you search.

**Index schema example — fisheries documents:**
```json
{
  "name": "fisheries-index",
  "fields": [
    {"name": "id",              "type": "Edm.String",              "key": true},
    {"name": "title",           "type": "Edm.String",              "searchable": true},
    {"name": "content",         "type": "Edm.String",              "searchable": true},
    {"name": "author",          "type": "Edm.String",              "filterable": true},
    {"name": "year",            "type": "Edm.Int32",               "filterable": true, "sortable": true},
    {"name": "key_phrases",     "type": "Collection(Edm.String)",  "searchable": true},
    {"name": "organizations",   "type": "Collection(Edm.String)",  "filterable": true},
    {"name": "content_vector",  "type": "Collection(Edm.Single)",  "searchable": true,
     "dimensions": 1536, "vectorSearchProfile": "my-profile"}
  ]
}
```

**Field attributes explained:**

| Attribute | Meaning | Example use |
|-----------|---------|-------------|
| `searchable` | Full-text search on this field | Search inside document content |
| `filterable` | Filter results by exact value | `year eq 2025` |
| `sortable` | Sort results by this field | Sort by date descending |
| `facetable` | Group results by this field | "Show counts by year" |
| `retrievable` | Return this field in results | Return title and author |
| `key` | Unique identifier for each document | Document ID |

---

### 4.5 Search Application — The User-Facing Layer

**What it is:** Your code (Python, JavaScript, .NET, etc.) that sends queries to the index and returns results to the user.

**REST API example:**
```python
import requests

endpoint  = "https://my-search.search.windows.net"
api_key   = "your-admin-key"
index     = "fisheries-index"

# Simple keyword search
response = requests.post(
    f"{endpoint}/indexes/{index}/docs/search?api-version=2024-07-01",
    headers={"api-key": api_key, "Content-Type": "application/json"},
    json={
        "search":  "total catch boat gear 2025",
        "top":     5,
        "select":  "title, content, key_phrases, year"
    }
)
results = response.json()["value"]
```

**Python SDK example (used in SmartSQL):**
```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name="nfisvctorindexwithparameter1",
    credential=AzureKeyCredential(SEARCH_KEY)
)

# Vector search — find similar SQL patterns
results = client.search(
    search_text="total catch by boat gear",
    vector_queries=[{
        "kind":   "text",
        "text":   "total catch by boat gear",
        "fields": "content_vector",
        "k":      5
    }],
    query_type="semantic",
    semantic_configuration_name="azureml-default",
    top=5
)
```

---

## 5. Index vs Indexer vs Indexing — The three words that confuse everyone

This is one of the most common points of confusion. Here is the clearest possible explanation:

```
INDEXING (the action)
  ↓
  "The process of reading your raw data and loading it into a searchable store"
  Like: scanning books and putting them in the library system
  Verb: "We are indexing the fisheries documents right now."

INDEXER (the worker — a noun)
  ↓
  "The Azure component that performs the indexing action"
  Like: the librarian who does the scanning
  Noun: "The indexer runs every 2 hours and processes new documents."
  In Azure Portal: Settings → Indexers

INDEX (the result — a noun)
  ↓
  "The searchable database that was created by the indexing process"
  Like: the card catalogue that was built from scanning all the books
  Noun: "The index now contains 10,000 searchable documents."
  In Azure Portal: Settings → Indexes
```

**One sentence to remember:**
> The **indexer** performs **indexing** to populate the **index**.

**Real analogy:**
- The **scanner** (indexer) scans each book page by page (indexing) and builds the library catalogue (index).
- Once built, you search the catalogue (index), not the books directly.
- The scanner can run again whenever new books arrive, updating the catalogue.

---

## 6. Pricing Tiers

Tiers include Free, Basic, Standard, and Storage Optimized. Standard and Storage Optimized are available with several configurations and capacities.

### Tier overview

| Tier | Best for | Max indexes | Max docs | Storage | SLA |
|------|----------|-------------|----------|---------|-----|
| **Free** | Learning, testing | 3 | 10,000 | 50 MB | No SLA |
| **Basic** | Small apps, proof-of-concept | 15 | 1M | 2 GB / partition | Yes (3 replicas) |
| **S1** | Production apps | 50 | 25M | 25 GB / partition | Yes |
| **S2** | Large workloads | 200 | 200M | 100 GB / partition | Yes |
| **S3** | Very large / complex | 200 | 200M | 200 GB / partition | Yes |
| **S3 HD** | Multi-tenant (many small indexes) | 1,000+ | 1M per index | 200 GB / partition | Yes |
| **L1** | Large infrequent queries | 10 | 160M | 1 TB / partition | Yes |
| **L2** | Largest datasets | 10 | 160M | 2 TB / partition | Yes |

### Tier selection guide — which tier for which situation?

```
Starting out / learning?
  → FREE — free forever, 1 per subscription, not for production

Building a pilot or small app (< 1M documents)?
  → BASIC — cheapest billable tier, supports SLA with 3 replicas
  → Used in SmartSQL for the SQL pattern index

Production app with standard load?
  → S1 — the most commonly used production tier

Large enterprise with millions of documents?
  → S2 or S3 — more storage, more capacity

Hosting a SaaS app with hundreds of customers each needing their own index?
  → S3 HD — designed for multi-tenancy (many small indexes)

100+ GB data that doesn't change much?
  → L1 or L2 — lower cost per TB than Standard
```

### SLA requirements

Service level agreements (SLAs) apply to billable services having two or more replicas for query workloads, or three or more replicas for query and indexing workloads. The number of partitions is not an SLA consideration.

---

## 7. Capacity Management

### The three key concepts

#### Replica — Computing power

**Simple explanation:** A replica is one copy of your search index running on one server. Adding more replicas means more servers answering queries in parallel.

Think of it like **checkout counters in a supermarket**:
- 1 replica = 1 checkout counter. Fine for a quiet shop.
- 3 replicas = 3 checkout counters. Handles the rush hour crowd.
- More replicas = more queries per second, lower latency, high availability.

> **Rule:** You need **at least 2 replicas** for query SLA. **At least 3 replicas** if you also want SLA during indexing.

#### Partition — Storage capacity

**Simple explanation:** A partition is a slice of storage. Adding more partitions gives you more space and faster ingestion of new data.

Think of it like **shelves in a library**:
- 1 partition = enough shelf space for your current collection.
- 2 partitions = double the shelf space. Same library, more books.
- More partitions = more documents, faster bulk indexing.

> **Rule:** Add partitions when you are running out of storage or when bulk indexing is slow.

#### Search Unit (SU) — The billing unit

**Simple explanation:** A Search Unit is one replica × one partition. It is how Azure counts and charges you.

One replica (compute node) × one partition (storage) is one Search Unit (SU). Because that multiplication is linear, a two-by-two topology costs four times as much as the starter one-by-one.

**The formula:**
```
Search Units = Replicas × Partitions
Cost per month = Search Units × Tier rate per SU
```

### Visual examples

```
EXAMPLE 1 — Starter (1 × 1 = 1 SU)
┌──────────┐
│ Replica 1│  ← 1 server answering queries
│ Partition│  ← 1 storage slice
└──────────┘
  Cost: 1 × $100 = $100/month (hypothetical)

─────────────────────────────────────────────

EXAMPLE 2 — High Availability (3 × 1 = 3 SU)
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Replica 1│ │ Replica 2│ │ Replica 3│  ← 3 servers, handles load + SLA
│ Partition│ │ Partition│ │ Partition│  ← same storage, replicated 3x
└──────────┘ └──────────┘ └──────────┘
  Cost: 3 × $100 = $300/month

─────────────────────────────────────────────

EXAMPLE 3 — High Storage (2 × 2 = 4 SU)
┌──────────┐ ┌──────────┐
│ Replica 1│ │ Replica 2│  ← 2 servers
│ Part 1   │ │ Part 1   │  ← Each replica gets both partitions
│ Part 2   │ │ Part 2   │
└──────────┘ └──────────┘
  Cost: 4 × $100 = $400/month
  Capacity: 2× the storage of Example 2

─────────────────────────────────────────────

EXAMPLE 4 — Enterprise (4 × 3 = 12 SU)
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ Rep 1│ │ Rep 2│ │ Rep 3│ │ Rep 4│  ← 4 servers = high query throughput
│ P1   │ │ P1   │ │ P1   │ │ P1   │
│ P2   │ │ P2   │ │ P2   │ │ P2   │
│ P3   │ │ P3   │ │ P3   │ │ P3   │  ← 3 partitions = 3× the storage
└──────┘ └──────┘ └──────┘ └──────┘
  Cost: 12 × $100 = $1,200/month
  Best for: large enterprise with high query volume + large dataset
```

### When to add what

| Symptom | Solution | Why |
|---------|----------|-----|
| Queries are slow / timing out | Add **replicas** | More servers share the query load |
| Running out of storage | Add **partitions** | More storage space |
| Bulk indexing is slow | Add **partitions** | More shards = faster parallel ingestion |
| Need SLA for queries | Min **2 replicas** | Azure SLA requires it |
| Need SLA during indexing | Min **3 replicas** | Azure SLA requirement |
| App crashes under peak traffic | Add **replicas** | More compute = more concurrent queries |

### Scalability — scaling up vs scaling out

```
SCALE UP   = Move to a higher tier (Free → Basic → S1 → S2)
             More powerful hardware per SU
             Required for: more indexes, more documents per index,
                           bigger storage per partition
             Limitation: cannot downgrade tier (plan carefully)

SCALE OUT  = Add more replicas or partitions within the same tier
             More units of the same hardware
             Required for: more queries per second, more storage,
                           high availability
             Flexible: can add and remove replicas/partitions anytime
```

> **Best practice:** Start with the smallest tier that meets your index size and feature needs. Scale out (add replicas/partitions) to handle traffic. Only scale up when you need features or storage limits that only higher tiers provide.

---

## 8. Search Types

Azure AI Search supports four query types. Understanding when to use each is essential:

### Keyword search (BM25)
Matches documents containing the exact words in the query. Fast and precise.
```
Query: "boat gear catch 2025"
Matches: documents containing those exact words
Misses:  "vessel equipment harvest 2025" (same meaning, different words)
```

### Semantic search
Re-ranks results by meaning using a language model. Finds conceptually relevant results.
```
Query: "vessel equipment harvest 2025"
Matches: documents about "boat gear catch 2025" because same meaning
Better for: natural language questions, exploratory search
```

### Vector search
Converts query to a vector, finds documents with similar vectors.
```
Query vector: [0.23, -0.11, 0.87, ...]  ← "total catch by gear"
Finds:        documents with similar vectors even with different words
Used in:      SmartSQL — finds SQL patterns similar to user's question
```

### Hybrid search (vector + keyword combined)
Azure AI Search units combine to provide additional throughput and storage. To increase both storage and throughput, a customer would need to purchase four units. Hybrid search runs both keyword and vector search and merges the results using a fusion algorithm (RRF — Reciprocal Rank Fusion).

```
Best results because:
  ✓ Keyword search catches exact column names and specific terms
  ✓ Vector search catches conceptual similarity with different words
  ✓ Combined = precision + flexibility

Used in SmartSQL: query_type = "vector_simple_hybrid"
```

---

## 9. How I Used It in SmartSQL

In my SmartSQL project, Azure AI Search plays the RAG role — it stores SQL query patterns and retrieves the most relevant ones for each user question.

### What is stored in the index

Not raw data — only SQL pattern examples:
```sql
-- Pattern 1: Total by category and time
SELECT gear_type, SUM(catch_kg) AS total_catch
FROM landings
WHERE YEAR(landing_date) = 2025
GROUP BY gear_type

-- Pattern 2: Count with filter
SELECT COUNT(*) AS total FROM landings
WHERE site_name LIKE '%northern%'
```

### The configuration used

```python
# In llm_langchain.py — extra_body attached via .bind()
_RAG_EXTRA_BODY = {
    "data_sources": [{
        "type": "azure_search",
        "parameters": {
            "endpoint":   SEARCH_ENDPOINT,
            "index_name": "nfisvctorindexwithparameter1",
            "authentication": {"type": "api_key", "key": SEARCH_KEY},
            "embedding_dependency": {
                "type":            "deployment_name",
                "deployment_name": "text-embedding-ada-002"
            },
            "query_type":      "vector_simple_hybrid",  # hybrid: vector + keyword
            "in_scope":        True,
            "strictness":      3,           # relevance filter (1-5)
            "top_n_documents": 5,           # return 5 most similar patterns
        }
    }]
}
LLM = AzureChatOpenAI(...).bind(extra_body=_RAG_EXTRA_BODY)
```

### Why this is secure

The index contains **only SQL patterns** — no actual fisheries data.  
If the index were compromised, an attacker would only see example SQL queries.  
All real data stays in the local database, queried only after the SQL is generated.

---

## 10. Interview Q&A

### "What is Azure AI Search?"

Azure AI Search is Microsoft's fully managed search-as-a-service. It allows you to index any data source — blobs, SQL, Cosmos DB — and make it searchable using keywords, semantic understanding, or vector similarity. In my SmartSQL project I used it for RAG: storing SQL query patterns as vectors and retrieving the 5 most similar patterns to guide GPT-4o-mini when generating SQL.

### "Explain the difference between an index and an indexer."

The indexer is the process — the worker that reads your raw data, optionally enriches it through a skillset, and loads it into the index. The index is the result — the searchable, structured store of your processed content. You only search the index, never the raw data source directly.

### "What is a Search Unit?"

A Search Unit is the billing unit. You are charged for the minimum required replica and partition combination (R × P) at the prorated hourly rate of your pricing tier. One replica times one partition equals one SU. Four replicas times three partitions equals twelve SUs, costing twelve times the base unit rate.

### "When would you add replicas vs partitions?"

Add replicas when queries are slow or you need high availability — replicas add compute (more servers answering queries in parallel). Add partitions when you need more storage or faster bulk indexing — partitions add storage capacity. The two scale independently and can be adjusted at any time within the same tier.

### "What is hybrid search and why did you use it?"

Hybrid search combines keyword search (BM25) and vector search. Keyword search is precise — it matches exact terms like column names. Vector search is flexible — it matches semantically similar content even with different words. Combining both gives the best result: I used `vector_simple_hybrid` in SmartSQL so that specific SQL terms like column names are matched exactly, while conceptual similarity (different ways of phrasing the same question) is also captured.

---

## 11. What to learn next

This is Part 1 of 8 in the Azure AI learning series. Recommended path:

| Part | Topic | Why it matters |
|------|-------|---------------|
| **1** | **Azure AI Search** ← you are here | Foundation for all RAG systems |
| 2 | Azure OpenAI Service | GPT-4, embeddings, prompt engineering |
| 3 | Azure AI Foundry | Model deployment, fine-tuning, hub |
| 4 | Azure Content Safety | Responsible AI, harm detection |
| 5 | Azure Cognitive Services | Vision, Speech, Language APIs |
| 6 | Azure Machine Learning | Custom model training, MLOps |
| 7 | Azure Bot Service | Chatbots, Teams integration |
| 8 | Azure AI Architecture Patterns | RAG, agents, multi-modal AI |

> Each part will be added to this `learning-guides/Azure-AI/` folder.  
> Parts 2–4 are directly related to the SmartSQL project and will be covered next.

---

## Resources

- [Official docs: Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [Pricing page](https://azure.microsoft.com/en-us/pricing/details/search/)
- [Service limits by tier](https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity)
- [Skillset reference](https://learn.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills)
- [SmartSQL project](../projects/smartSQL.md) — real production usage of Azure AI Search

---

*Part of the Azure AI learning series by [Irshad Vaza](https://irshadvaza.tech)*  
*Contact: aiandsmartdata@gmail.com*
