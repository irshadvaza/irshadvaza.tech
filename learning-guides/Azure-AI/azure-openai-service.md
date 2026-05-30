# Azure OpenAI Service — Complete Guide

> **Learning Guide** · Azure AI Series · Part 2 of 8  
> Author: Irshad Vaza · AI & Data Specialist · [irshadvaza.tech](https://irshadvaza.tech)  
> Last updated: 2025 · Reflects latest Azure AI Foundry model availability

[![Azure](https://img.shields.io/badge/Azure-OpenAI_Service-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Level](https://img.shields.io/badge/Level-Beginner_to_Expert-brightgreen)](.)
[![Real Project](https://img.shields.io/badge/Used_in-SmartSQL_Project-purple)](../projects/smartSQL.md)

---

## Table of Contents

1. [What is Azure OpenAI Service?](#1-what-is-azure-openai-service)
2. [Azure OpenAI vs OpenAI direct — why pay more?](#2-azure-openai-vs-openai-direct--why-pay-more)
3. [What is a Token?](#3-what-is-a-token--the-currency-of-llms)
4. [What is a Context Window?](#4-what-is-a-context-window)
5. [Model catalogue — every model explained](#5-model-catalogue)
6. [Embeddings — turning text into numbers](#6-embeddings--turning-text-into-numbers)
7. [Deployment types — Pay-as-you-go vs PTU](#7-deployment-types)
8. [Pricing — how you get billed](#8-pricing)
9. [Temperature and other parameters](#9-temperature-and-other-parameters)
10. [API versions and how to call the API](#10-api-versions-and-calling-the-api)
11. [Why SmartSQL uses BOTH Azure AI Search AND Azure OpenAI](#11-why-smartsql-uses-both-azure-ai-search-and-azure-openai)
12. [Interview Q&A](#12-interview-qa)
13. [What to learn next](#13-what-to-learn-next)

---

## 1. What is Azure OpenAI Service?

**Simple answer:** Azure OpenAI Service lets you use OpenAI's AI models (like ChatGPT and DALL-E) inside Microsoft Azure — with enterprise security, compliance, and private networking.

**Technical answer:** Azure OpenAI Service is a managed platform from Microsoft that provides access to OpenAI's language models — including GPT-4o, GPT-4o-mini, and the o-series reasoning models — through REST APIs. Developers can integrate natural language processing, text summarisation, code generation, semantic search, image generation, and audio capabilities into their applications while benefiting from Azure's reliability, scalability, and enterprise security controls.

**The key distinction:** Unlike the publicly accessible OpenAI API, Azure OpenAI integrates natively with other Azure resources — Azure AI Search, Key Vault, Monitor, private networking — giving enterprises finer control over model deployment, data handling, and compliance.

```
OpenAI (openai.com)          Azure OpenAI Service
─────────────────────        ──────────────────────────────────
Same GPT-4o model    ←───────── Same model, different wrapper
Public internet              Private Azure network
No compliance certs          SOC 2, HIPAA, FedRAMP, ISO 27001
Shared infrastructure        Dedicated capacity available
No Azure integration         Native Azure AI Search, Key Vault,
                             Monitor, Defender integration
Best for: startups,          Best for: government, healthcare,
  personal projects,           banking, regulated industries,
  experimentation              enterprise production systems
```

> **In SmartSQL:** We use Azure OpenAI (not direct OpenAI) because the application is built for a government environmental agency. Data residency and compliance requirements mandate Azure-hosted services.

---

## 2. Azure OpenAI vs OpenAI Direct — Why Pay More?

Token pricing between Azure and OpenAI direct is identical. The total cost runs 15–40% higher on Azure due to support plans, data transfer, storage, and network infrastructure. For regulated industries, the premium is not optional — it is mandatory.

Here is what you get for the premium:

| Feature | OpenAI direct | Azure OpenAI |
|---------|--------------|--------------|
| Private networking (VNet) | ❌ | ✅ |
| Enterprise SLA 99.9% | ❌ | ✅ |
| SOC 2, HIPAA, FedRAMP | ❌ | ✅ |
| Regional data residency | ❌ | ✅ (UAE, EU, US, Asia) |
| Azure Monitor integration | ❌ | ✅ |
| Azure Key Vault for secrets | ❌ | ✅ |
| Managed Identity auth | ❌ | ✅ |
| Azure Defender security | ❌ | ✅ |
| RBAC via Entra ID | ❌ | ✅ |
| Content filtering built-in | Limited | ✅ Full Azure Content Safety |

---

## 3. What is a Token? — The Currency of LLMs

**Simple explanation:** A token is a chunk of text. Not a word, not a character — somewhere in between. AI models do not read words the way humans do. They break text into tokens, process each token, and generate tokens in response.

**The rule of thumb:**
```
~1 token = ~4 characters of English text
~1 token = ~0.75 words
1,000 tokens ≈ 750 words ≈ one page of text
```

**Real examples:**
```
"hello"              → 1 token
"Hello, world!"      → 4 tokens
"SmartSQL"           → 2 tokens  (Smart + SQL)
"tpep_pickup_datetime" → 6 tokens (unusual compound words split into more tokens)
```

**Why tokens matter:** Every API call to Azure OpenAI is billed per token — both tokens you send in (input tokens) and tokens the model generates back (output tokens). More tokens = higher cost + higher latency.

**Input vs Output tokens:**
```
INPUT TOKENS  = everything you send to the model:
  - System prompt
  - Chat history (conversational memory)
  - RAG context (retrieved SQL patterns)
  - User's question
  → Billed at input rate (cheaper)

OUTPUT TOKENS = everything the model generates back:
  - The SQL query
  - Any explanation text
  → Billed at output rate (more expensive, ~2-3x input price)
```

**Cost calculation example for SmartSQL:**
```
One SmartSQL query breakdown:
  System prompt:          ~300 tokens  (rules + schema description)
  5 RAG SQL patterns:     ~500 tokens  (retrieved SQL examples)
  User question:          ~10 tokens   ("total catch by boat gear 2025")
  ─────────────────────────────────────
  Total INPUT:            ~810 tokens

  Generated SQL response: ~50 tokens   (SELECT gear_type, SUM...)
  Total OUTPUT:           ~50 tokens

  Total per query:        ~860 tokens
  At GPT-4o-mini rate:   ~$0.00013 per query
  1,000 queries/month:    ~$0.13/month  ← very cheap!
```

---

## 4. What is a Context Window?

**Simple explanation:** The context window is the maximum amount of text an AI model can read at one time. It is like the model's "short-term memory" — everything within the window is what the model can "see" when generating a response.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW (128K tokens)                  │
│                                                                  │
│  System prompt    │  Chat history  │  RAG context  │  Question  │
│  (300 tokens)     │  (200 tokens)  │  (500 tokens) │  (10 tok)  │
│                                                                  │
│  Everything here is what GPT-4o-mini can "see" right now        │
└─────────────────────────────────────────────────────────────────┘
                               ▼
                     Generates response
                     (SQL query — ~50 tokens)
```

**Why context window size matters:**
- Larger window = can handle longer documents, longer conversations, more RAG examples
- Larger window = more tokens processed = higher cost per call
- SmartSQL uses ~860 tokens per call — well within the 128K limit

**Model context windows:**

| Model | Context window | Best for |
|-------|---------------|---------|
| GPT-4o-mini | 128K tokens | SmartSQL — balance of cost and capability |
| GPT-4o | 128K tokens | Complex reasoning, vision tasks |
| o3-mini | 200K tokens | Deep reasoning problems, long documents |
| text-embedding-ada-002 | 8K tokens | Converting text to vectors |
| text-embedding-3-small | 8K tokens | Faster, cheaper embeddings |
| text-embedding-3-large | 8K tokens | Highest quality embeddings |

> **Practical rule:** Context window = tokens IN + tokens OUT combined. If your prompt alone is 100K tokens, you only have 28K tokens left for the model to generate a response (in a 128K model).

---

## 5. Model Catalogue

Azure OpenAI provides several model families, each designed for different tasks.

### 5.1 GPT models — Text generation and chat

**GPT-4o (Omni) — The flagship**
```
What:    Most capable multimodal model. Handles text + images + audio.
Context: 128K tokens
Use for: Complex analysis, vision tasks, document understanding,
         high-stakes reasoning where accuracy matters most
Cost:    Higher than 4o-mini
Example: "Analyse this satellite image and extract all vessel positions"
```

**GPT-4o-mini — The workhorse ← Used in SmartSQL**
```
What:    Smaller, faster, cheaper version of GPT-4o. Still very capable.
Context: 128K tokens
Use for: SQL generation, chatbots, classification, summarisation,
         any task where cost-efficiency matters more than raw capability
Cost:    ~60x cheaper than GPT-4 Turbo — most cost-efficient small model
         with vision capabilities
SmartSQL: Chosen for SQL generation because:
          - SQL is structured and deterministic — doesn't need full GPT-4
          - RAG provides examples so the model doesn't need to guess
          - 128K context handles our prompt + history comfortably
          - At ~$0.00013/query, 10,000 queries costs ~$1.30
```

**o3-mini, o4-mini — Reasoning models**
```
What:    Designed for multi-step reasoning and complex problem solving.
         "Thinks" before answering — uses chain-of-thought internally.
Context: 200K tokens (o3-mini)
Use for: Math, science, coding challenges, legal/financial analysis,
         any task requiring deep logical reasoning
Cost:    Higher than GPT-4o-mini, lower than o3
Example: "Find the bug in this 500-line Python algorithm"
NOT for: Simple tasks like SQL generation — overkill and overpriced
```

### 5.2 Embedding models — Text to vectors

Embedding models are fundamentally different from GPT models. They do not generate text. They convert text into a list of numbers (a vector) that represents the meaning of the text.

**text-embedding-ada-002 ← Used in SmartSQL**
```
What:    Converts text to a 1,536-dimension vector
Cost:    Very cheap — ~$0.0001 per 1K tokens
Use for: Semantic search, RAG pipelines, similarity matching
SmartSQL: Converts user questions and SQL patterns into vectors
          so Azure AI Search can find similar SQL patterns
```

**text-embedding-3-small**
```
What:    Newer, faster, cheaper than ada-002. 1,536 dimensions.
Cost:    ~5x cheaper than ada-002
Use for: High-volume embedding generation where cost is critical
When:    Use this for new projects instead of ada-002
```

**text-embedding-3-large**
```
What:    Highest quality embeddings. 3,072 dimensions.
Cost:    ~3x more than 3-small
Use for: When search quality matters most — legal, medical, research
When:    Use when ada-002 or 3-small miss too many relevant results
```

### 5.3 Image models

**gpt-image-1 (DALL-E 4)**
```
What:    Generates images from text prompts
Use for: Marketing content, product visualisation, design prototyping
Example: "Generate a professional dashboard screenshot for a fishing data app"
```

### 5.4 Audio models

**GPT-4o Realtime**
```
What:    Speech-to-speech in real time, low latency
Use for: Voice assistants, call centre bots, live captioning
SmartSQL connection: The voice input in SmartSQL uses Google STT instead
                    of this model — but Azure Realtime is the enterprise
                    alternative for production voice features
```

**Whisper (transcribe-mini)**
```
What:    Speech-to-text (transcription), not real-time
Use for: Transcribing meeting recordings, podcasts, audio files
```

---

## 6. Embeddings — Turning Text Into Numbers

This section is critical for understanding RAG and why SmartSQL works the way it does.

### What is an embedding?

An embedding is a list of numbers — a vector — that represents the meaning of a piece of text. Two pieces of text that mean the same thing will have similar vectors, even if the words are completely different.

```
"show total catch by boat gear"    → [0.23, -0.11, 0.87, 0.45, ...]  ← 1,536 numbers
"display aggregate by vessel type" → [0.24, -0.10, 0.86, 0.44, ...]  ← similar!

"quarterly revenue by product"     → [0.91, 0.33, -0.22, 0.78, ...]  ← very different
```

### Why 1,536 numbers?

The number 1,536 is the dimensionality of the vector space. Think of it as having 1,536 different "axes" of meaning. Each axis might loosely represent concepts like:
- Is this about time? (axis 1)
- Is this about fishing? (axis 2)
- Is this a question? (axis 3)
- ... and 1,533 more abstract dimensions the model learned

No human defined these axes. The model learned them from billions of text examples during training.

### How similarity is measured

To find similar vectors, Azure AI Search computes the **cosine similarity** — essentially the angle between two vectors. Vectors pointing in the same direction (small angle) are similar. Vectors pointing in opposite directions (large angle) are very different.

```
Cosine similarity = 1.0  → identical meaning
Cosine similarity = 0.9  → very similar
Cosine similarity = 0.5  → somewhat related
Cosine similarity = 0.0  → unrelated
Cosine similarity = -1.0 → opposite meaning
```

### The embedding pipeline in SmartSQL

```
INDEXING TIME (done once, when building the index):
  SQL pattern text
  "SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type"
         │
         ▼
  text-embedding-ada-002
         │
         ▼
  Vector: [0.23, -0.11, 0.87, ...]  (1,536 numbers)
         │
         ▼
  Stored in Azure AI Search index
  (SQL text + vector stored together)

──────────────────────────────────────────────────────────

QUERY TIME (every user question):
  User question: "show catch breakdown by gear type"
         │
         ▼
  text-embedding-ada-002
         │
         ▼
  Question vector: [0.22, -0.12, 0.85, ...]
         │
         ▼
  Azure AI Search: "find the 5 stored vectors most similar to this"
         │
         ▼
  Returns: Top 5 most similar SQL patterns
         │
         ▼
  These 5 patterns go into the GPT-4o-mini prompt as examples
```

### Why this makes SQL generation accurate

Without RAG:
```
User: "show catch breakdown by gear type"
GPT-4o-mini (without examples): Might guess:
  SELECT equipment_category, total FROM fisheries  ← wrong column names!
```

With RAG:
```
User: "show catch breakdown by gear type"
Retrieved example: SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type
GPT-4o-mini (with example): Generates:
  SELECT gear_type, SUM(catch_kg) FROM landings
  WHERE YEAR(landing_date) = 2025
  GROUP BY gear_type
  ORDER BY SUM(catch_kg) DESC    ← correct column names, correct table!
```

The embedding model does not generate SQL — it enables finding relevant examples. The GPT model then uses those examples to write accurate SQL.

---

## 7. Deployment Types

When you deploy a model in Azure OpenAI, you choose a deployment type. This determines billing and performance characteristics.

### Standard (Pay-as-you-go)

```
How it works: Pay per token consumed. No upfront commitment.
              You pay only for what you use.
Best for:     Development, testing, low/variable traffic,
              experimentation, pilot projects

Pros:
  ✓ No upfront cost — start immediately
  ✓ Scale to zero (no traffic = no cost)
  ✓ Flexible — change models anytime

Cons:
  ✗ Variable latency under high load
  ✗ Subject to rate limits (TPM = tokens per minute)
  ✗ Can be throttled during peak Azure-wide usage

SmartSQL uses: Standard deployment
Reason: Variable traffic (demo + development), cost flexible
```

### Global Standard

```
How it works: Same pay-per-token as Standard, but traffic is
              routed globally to the nearest available datacenter.
Best for:     Higher throughput needs, when your region has
              limited capacity for the model you need

Pros:
  ✓ Higher throughput limits than regional Standard
  ✓ Access to models not yet available in your region

Cons:
  ✗ Data may leave your preferred region (check compliance)
```

### Provisioned (PTU — Provisioned Throughput Units)

```
How it works: Reserve dedicated model processing capacity.
              You pay for the reserved capacity regardless of
              whether you use it (like renting office space).
Best for:     Production apps with consistent, high traffic
              (typically > 300M tokens/month)

PTU = unit of reserved compute capacity
      billed hourly based on number of PTUs deployed
      NOT based on tokens consumed

Think of it like:
  Pay-as-you-go = taxi (pay per km, available when needed)
  PTU           = leased car (monthly cost, always available,
                  cheaper per km at high mileage)

Pros:
  ✓ Consistent, predictable latency
  ✓ No throttling — capacity is exclusively yours
  ✓ Cost-effective at high, steady volume
  ✓ Reservation discounts for 1-year commitments

Cons:
  ✗ You pay even when idle (no traffic = still charged)
  ✗ Minimum commitment (~$2,448/month starting)
  ✗ PTU quota ≠ guaranteed capacity at time of deployment

When to switch from Standard to PTU:
  Break-even typically occurs around 300M-500M tokens/month.
  Below that, Standard wins on simplicity and cost.
```

### Deployment type decision guide

```
Monthly tokens < 50M?     → Standard (pay-as-you-go)
Monthly tokens 50M-300M?  → Standard + optimise prompts
Monthly tokens > 300M?    → Evaluate PTU vs Standard
Need consistent latency?  → PTU regardless of volume
Building a pilot?         → Always start with Standard
Production enterprise?    → Benchmark Standard first, then PTU
```

---

## 8. Pricing

### How billing works

Every Azure OpenAI call is billed on tokens. You are charged for the minimum required token consumption at the prorated rate of your chosen model.

```
Cost = (Input tokens × input rate) + (Output tokens × output rate)
```

Output tokens are more expensive than input tokens because generating text requires more compute than reading text.

### Approximate pricing reference (check Azure portal for current rates)

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best for |
|-------|----------------------|------------------------|---------|
| GPT-4o-mini | ~$0.00015 | ~$0.0006 | SmartSQL, chatbots, classification |
| GPT-4o | ~$0.005 | ~$0.015 | Complex reasoning, vision |
| o3-mini | ~$0.001 | ~$0.004 | STEM, deep reasoning |
| text-embedding-ada-002 | ~$0.0001 | — | RAG indexing |
| text-embedding-3-small | ~$0.00002 | — | High-volume RAG |

> **Note:** Prices change frequently. Always check the [Azure pricing page](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) for current rates.

### Real cost example — SmartSQL at scale

```
Scenario: 10,000 queries/month on GPT-4o-mini

Per query:
  Input:  810 tokens × $0.00015/1K = $0.000122
  Output: 50 tokens  × $0.0006/1K  = $0.000030
  Total per query:                    $0.000152

Monthly cost:
  10,000 queries × $0.000152 = $1.52/month

With embeddings (for RAG indexing — done once):
  500 SQL patterns × ~100 tokens = 50,000 tokens
  50,000 × $0.0001/1K = $0.005  ← negligible one-time cost

Total SmartSQL monthly cost: ~$1.52 + Azure AI Search Basic tier
```

### Cost optimisation strategies

```
1. PROMPT CACHING
   Azure caches repeated prompt prefixes automatically.
   Structure prompts so the system prompt (static) comes first.
   The variable part (question) comes last.
   Cached input tokens cost 50% less.
   SmartSQL benefits: system prompt (300 tokens) is cached on
   every call → saves ~$0.60 per 10,000 queries

2. CHOOSE THE RIGHT MODEL
   GPT-4o-mini instead of GPT-4o for structured tasks like SQL:
   ~30x cost reduction with comparable accuracy on structured tasks

3. LOW TEMPERATURE
   temperature=0.3 in SmartSQL reduces token waste from
   "creative" verbose responses — model is more concise

4. BATCH API (for non-real-time workloads)
   Non-interactive large-volume workloads can use Batch API:
   up to 50% discount, results returned within 24 hours
   Not suitable for SmartSQL (real-time queries) but great for:
   nightly processing, content generation, document analysis

5. CONTEXT WINDOW MANAGEMENT
   Limit conversational history to last N turns only.
   Don't send the entire chat history for every new question.
   SmartSQL: last 4 turns kept in context (not all history)
```

---

## 9. Temperature and Other Parameters

These are the settings you pass when calling the API. Understanding them is essential for consistent AI behaviour.

### Temperature — randomness control

```
Temperature = how "creative" or "random" the model's output is.
Range: 0.0 to 2.0

temperature=0.0  Completely deterministic. Same input → same output
                 every single time. Used for: automated testing,
                 financial calculations, legal text generation.

temperature=0.3  Mostly deterministic with slight variation.
                 ← SmartSQL uses this.
                 Good for: SQL generation, code, structured tasks.
                 Why 0.3 not 0.0? Tiny variation helps avoid getting
                 stuck on the same wrong SQL pattern repeatedly.

temperature=0.7  Balanced. Good for: chat, summarisation, Q&A.
                 Default value in most APIs.

temperature=1.0  Creative and varied. Good for: brainstorming,
                 story writing, diverse suggestions.

temperature=1.5  Very creative, sometimes incoherent.
                 Good for: poetry, experimental content.

temperature=2.0  Very random. Rarely useful in production.
```

**Why SQL generation uses low temperature:**
```
User: "total catch by gear type"

temperature=0.7 might generate different SQL each time:
  Run 1: SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type
  Run 2: SELECT g.type, SUM(l.weight) FROM landings l ...  ← different aliases
  Run 3: SELECT gear_type, COUNT(*) FROM landings ...  ← wrong aggregation!

temperature=0.3 generates consistent SQL:
  Run 1: SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type
  Run 2: SELECT gear_type, SUM(catch_kg) FROM landings GROUP BY gear_type
  ← same result every time
```

### Other key parameters

```python
# SmartSQL API call — all parameters explained
completion = client.chat.completions.create(
    model="gpt-4o-mini",

    messages=[...],             # The conversation: system + history + question

    temperature=0.3,            # Low = consistent SQL (0.0-2.0)

    max_tokens=800,             # Maximum tokens in the response.
                                # Set a limit to prevent runaway costs.
                                # SQL queries are short — 800 is plenty.

    top_p=0.95,                 # Nucleus sampling. Alternative to temperature.
                                # 0.95 = consider tokens covering 95% of
                                # probability mass. Usually leave at 0.95.

    frequency_penalty=0,        # Penalise repeating the same words.
                                # 0 = no penalty. Range: -2.0 to 2.0.
                                # Rarely changed for SQL generation.

    presence_penalty=0,         # Penalise introducing new topics.
                                # 0 = no penalty. Range: -2.0 to 2.0.
                                # Rarely changed for SQL generation.

    stream=False,               # False = wait for full response.
                                # True = stream tokens as they arrive
                                #        (like ChatGPT typing effect).
)
```

---

## 10. API Versions and Calling the API

### API versioning

Azure OpenAI uses date-based API versions. Using the wrong version can cause errors like "Extra inputs are not permitted" (the `max_tokens` vs `max_completion_tokens` issue encountered in SmartSQL).

```
API version             What changed
─────────────────────────────────────────────────────────────
2023-05-15              Original GA version
2023-12-01-preview      Added functions, tools support
2024-02-15-preview      Stable — used in SmartSQL.
                        Accepts max_tokens (not renamed yet).
2024-05-01-preview      Renamed max_tokens → max_completion_tokens.
                        SmartSQL hit this bug initially.
2024-07-01              Current GA version for most features.
2024-12-01-preview      Latest features including o-series reasoning
```

**Lesson from SmartSQL:** Pin your `api_version` explicitly. Changing it automatically as Azure updates can break your application with parameter name changes.

### Calling the API — three ways

**Method 1: Direct REST (any language)**
```python
import requests, os

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
key      = os.getenv("AZURE_OPENAI_API_KEY")

response = requests.post(
    f"{endpoint}/openai/deployments/gpt-4o-mini/chat/completions"
    "?api-version=2024-02-15-preview",
    headers={
        "Content-Type": "application/json",
        "api-key": key
    },
    json={
        "messages": [
            {"role": "system",  "content": "You generate SQL queries."},
            {"role": "user",    "content": "show total catch by gear"}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
)
sql = response.json()["choices"][0]["message"]["content"]
```

**Method 2: OpenAI Python SDK (with Azure config)**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key        = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version    = "2024-02-15-preview"
)

completion = client.chat.completions.create(
    model       = "gpt-4o-mini",     # deployment name in Azure
    messages    = [
        {"role": "system", "content": "You generate SQL queries."},
        {"role": "user",   "content": "show total catch by gear"}
    ],
    temperature = 0.3,
    max_tokens  = 800
)
sql = completion.choices[0].message.content
```

**Method 3: LangChain (used in SmartSQL)**
```python
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create the LLM object
llm = AzureChatOpenAI(
    azure_endpoint    = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key           = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment  = "gpt-4o-mini",
    api_version       = "2024-02-15-preview",
    temperature       = 0.3,
    max_tokens        = 800,
).bind(extra_body=RAG_CONFIG)   # attach Azure AI Search

# Build the chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You generate SQL queries. Rules: SELECT only."),
    ("human",  "{question}"),
])

chain = prompt | llm | StrOutputParser()

# Call it
sql = chain.invoke({"question": "show total catch by gear"})
```

**Why LangChain for SmartSQL?** LangChain wraps the SDK call with composable steps, making it easy to add validation before and after the LLM call, swap models with one line, enable tracing, and build the memory-aware chain with `RunnableWithMessageHistory`.

---

## 11. Why SmartSQL Uses BOTH Azure AI Search AND Azure OpenAI

This is the most important section for portfolio and interview purposes — understanding why two separate Azure services work together.

### The problem each service solves

```
Azure OpenAI alone:
  + Brilliant language understanding and generation
  - Has no idea what your database looks like
  - Guesses table names and column names from training data
  - Generates plausible-looking SQL that runs but returns wrong data
  - Every query is independent — no memory of your schema

Azure AI Search alone:
  + Stores and finds your SQL patterns efficiently
  + Hybrid vector + keyword search
  - Cannot understand natural language questions
  - Cannot generate SQL
  - Is just a search engine, not an AI

Together:
  Azure AI Search finds the most relevant SQL examples.
  Azure OpenAI uses those examples to generate accurate SQL.
  Each service does exactly what it is best at.
```

### The division of labour — step by step

```
User question: "show total catch by boat gear for Q2 of 2025"

─────────────────────────────────────────────────────────────
STEP 1: text-embedding-ada-002 (Azure OpenAI — embedding model)
─────────────────────────────────────────────────────────────
  Input:  "show total catch by boat gear for Q2 of 2025"
  Output: [0.23, -0.11, 0.87, 0.45, ...]  (1,536 numbers)
  Job:    Convert the question into a mathematical representation
          that captures its meaning

─────────────────────────────────────────────────────────────
STEP 2: Azure AI Search (vector search)
─────────────────────────────────────────────────────────────
  Input:  The question vector
  Searches: Index of pre-vectorised SQL patterns
  Output: Top 5 SQL patterns most similar to the question:
    Pattern 1: SELECT gear_type, SUM(catch_kg)...GROUP BY gear_type
    Pattern 2: SELECT gear_type, COUNT(*)...WHERE quarter=2...
    Pattern 3: SELECT site_name, SUM(catch_kg)...
    Pattern 4: SELECT gear_type, AVG(catch_kg)...
    Pattern 5: SELECT gear_type, catch_kg...WHERE year=2025
  Job:    Find relevant examples from your own data, fast

─────────────────────────────────────────────────────────────
STEP 3: GPT-4o-mini (Azure OpenAI — chat model)
─────────────────────────────────────────────────────────────
  Input:  System prompt + 5 SQL examples + user question
  Prompt:
    "You generate SQL. Rules: SELECT only. Use LIKE for strings.
     Here are similar SQL patterns from this database:
     [Pattern 1]
     [Pattern 2]
     [Pattern 3]
     [Pattern 4]
     [Pattern 5]
     Now answer: show total catch by boat gear for Q2 of 2025"
  Output: SELECT gear_type, SUM(catch_kg) AS total_catch
          FROM landings
          WHERE YEAR(landing_date) = 2025
            AND DATEPART(quarter, landing_date) = 2
          GROUP BY gear_type
          ORDER BY total_catch DESC
  Job:    Generate accurate SQL by adapting the most relevant example
```

### Why not just use GPT-4o without Azure AI Search?

```
Without RAG (GPT-4o-mini alone):
  User: "show total catch by boat gear for Q2 of 2025"
  GPT-4:  SELECT equipment_type, SUM(weight) FROM fish_data
          WHERE quarter = 2 AND year = 2025
          GROUP BY equipment_type
          ← "equipment_type" doesn't exist in our schema!
            "weight" doesn't exist — it's "catch_kg"!
            "fish_data" doesn't exist — it's "landings"!
  Result: SQL runs but returns an error or wrong data.

With RAG (Azure AI Search + GPT-4o-mini):
  Same question + retrieved patterns that use the REAL column names
  GPT-4:  SELECT gear_type, SUM(catch_kg) AS total_catch
          FROM landings
          WHERE YEAR(landing_date) = 2025
            AND DATEPART(quarter, landing_date) = 2
          GROUP BY gear_type
          ← Uses the REAL column names from the real schema!
  Result: SQL runs correctly and returns the right data.
```

### Why not just put the full schema in the prompt?

```
Option A: Full schema in system prompt (no RAG)
  Pro:  Simpler architecture
  Con:  Large tables with 50+ columns = huge prompt every call
        At 50 columns × 10 tables = ~2,000 tokens just for schema
        Every query costs 2,000 extra input tokens ≈ 20× more expensive
        Also: GPT still doesn't know which QUERY PATTERNS work with your data

Option B: RAG with SQL patterns (SmartSQL approach)
  Pro:  Only relevant patterns included (~500 tokens vs 2,000+)
        LLM sees working examples, not just column names
        More accurate than schema alone
        Lower cost per query
        Index is reusable — add patterns as new query types emerge
  Con:  Requires maintaining an Azure AI Search index
        Initial setup to populate SQL patterns

Verdict: For databases with complex schemas and many query patterns,
         RAG is more accurate, more scalable, and cheaper at volume.
```

### The architecture in one picture

```
                    ┌──────────────────────────────────────────┐
                    │           AZURE AI FOUNDRY                │
                    │                                          │
  User question     │   ┌─────────────────┐                   │
  "show catch ──────┼──►│ text-embedding  │                   │
   by gear"         │   │ ada-002         │                   │
                    │   │ (Embedding      │                   │
                    │   │  model)         │                   │
                    │   └────────┬────────┘                   │
                    │            │ question vector             │
                    │            ▼                             │
                    │   ┌─────────────────┐                   │
                    │   │ Azure AI Search  │                   │
                    │   │ (SQL pattern    │                   │
                    │   │  index)         │                   │
                    │   └────────┬────────┘                   │
                    │            │ 5 similar SQL patterns      │
                    │            ▼                             │
                    │   ┌─────────────────┐                   │
                    │   │  GPT-4o-mini    │                   │
                    │   │  (Chat model)   │◄── system prompt  │
                    │   │                 │    + schema desc   │
                    │   └────────┬────────┘                   │
                    │            │ generated SQL               │
                    └────────────┼─────────────────────────────┘
                                 │
                    ┌────────────▼─────────────────────────────┐
                    │       LOCAL ENVIRONMENT                   │
                    │  SQL validated → DuckDB / Azure SQL       │
                    │  Results returned to user                 │
                    └──────────────────────────────────────────┘
```

**The security boundary:** Only the question vector and generated SQL cross into Azure. Your actual data never leaves your local environment.

### Summary table — which service does what

| Task | Service | Model | Why |
|------|---------|-------|-----|
| Convert question to vector | Azure OpenAI | text-embedding-ada-002 | Creates comparable mathematical representation |
| Find similar SQL patterns | Azure AI Search | Vector index | Fast similarity search over stored patterns |
| Generate SQL from examples | Azure OpenAI | GPT-4o-mini | Language understanding + generation |
| Screen harmful input | Azure Content Safety | Built-in | 4 harm categories, jailbreak detection |
| Execute the SQL | DuckDB / Azure SQL | — | Local — data never goes to cloud |

---

## 12. Qestations & Answer for summary.

### "What is Azure OpenAI Service and how is it different from using OpenAI directly?"

Azure OpenAI Service provides the same models as OpenAI but hosted on Azure infrastructure with enterprise features — private networking, SOC 2 / HIPAA / FedRAMP compliance, regional data residency, and native integration with Azure services like Key Vault, Monitor, and AI Search. Token pricing is identical; total cost is 15–40% higher on Azure due to infrastructure overhead. For a government agency handling regulated environmental data, Azure OpenAI is the only compliant choice.

### "What is a token and why does it matter?"

A token is roughly four characters of text. Every API call is billed on the number of tokens sent in (input tokens) and generated back (output tokens). Output tokens are typically two to three times more expensive than input tokens. In SmartSQL, one query uses approximately 810 input tokens and 50 output tokens, costing about $0.00015 — making 10,000 queries cost around $1.50 per month.

### "Why did you choose GPT-4o-mini instead of GPT-4o?"

SQL generation is a structured, deterministic task. It does not require the full reasoning capability of GPT-4o. GPT-4o-mini at temperature 0.3 produces consistent, accurate SQL at approximately 30 times lower cost. The RAG pipeline compensates for any capability gap — by providing five proven SQL examples as context, the model adapts rather than guessing. Lower temperature also reduces token waste from verbose responses.

### "Explain the difference between an embedding model and a chat model."

A chat model generates text. You give it a prompt and it writes a response. A GPT-4o-mini is a chat model. An embedding model does not generate text — it converts text into a vector, a list of numbers representing the meaning of that text. text-embedding-ada-002 is an embedding model. In SmartSQL, the embedding model converts the user's question into a vector so Azure AI Search can find mathematically similar SQL patterns. The chat model then uses those patterns to write the actual SQL.

### "What is the difference between Standard and PTU deployment?"

Standard is pay-per-token — you pay only for what you use, flexible for variable traffic but latency can vary under load. PTU (Provisioned Throughput Units) is reserved capacity — you pay for the capacity whether you use it or not, like renting an office, but latency is consistent and predictable. The break-even point is typically 300–500 million tokens per month. SmartSQL uses Standard because it is a variable-traffic application and the monthly token volume is far below the PTU break-even point.

### "What does temperature do and why did you set it to 0.3?"

Temperature controls how random the model's output is, from 0.0 (completely deterministic) to 2.0 (very random). SQL generation needs to be consistent — the same question should produce the same SQL. I chose 0.3 rather than 0.0 because a tiny amount of variation helps avoid getting stuck on the same wrong pattern if the first attempt fails. At 0.0 the model would retry with the exact same output, which is not useful for the LangGraph auto-retry loop.

---

## 13. What to Learn Next

| Part | Topic | Why |
|------|-------|-----|
| ✅ 01 | Azure AI Search | Foundation for RAG |
| ✅ 02 | **Azure OpenAI Service** ← you are here | LLMs, embeddings, tokens |
| 🔜 03 | Azure AI Foundry | Where you deploy and manage models |
| 🔜 04 | Azure Content Safety | The safety layer used in SmartSQL |
| 🔜 05 | Azure Cognitive Services | Vision, Speech, Language APIs |
| 🔜 06 | Azure Machine Learning | Training, MLOps, custom models |
| 🔜 07 | Azure Bot Service | Chatbots and voice agents |
| 🔜 08 | Azure AI Architecture Patterns | How all services work together |

> **Recommended next:** Read [Part 03 — Azure AI Foundry](./azure-ai-foundry.md) to understand where GPT-4o-mini and text-embedding-ada-002 are deployed and managed, and how Azure AI Foundry is the central hub for all AI services used in SmartSQL.

---

## Resources

- [Azure OpenAI Service documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Pricing page](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [Model availability by region](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
- [Deployment types](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/deployment-types)
- [API reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- [SmartSQL project](../projects/smartSQL.md) — production usage of GPT-4o-mini + text-embedding-ada-002

---

*Part of the Azure AI learning series by [Irshad Vaza](https://irshadvaza.tech)*  
*Contact: aiandsmartdata@gmail.com*
