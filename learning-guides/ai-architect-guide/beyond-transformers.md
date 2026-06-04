# Beyond Transformers — The Next Generation of AI Architectures

> **Learning Guide** · AI Foundations Series
> Author: Irshad Vaza · AI & Data Specialist · [irshadvaza.tech](https://irshadvaza.tech)
> Last updated: 2025 · Beginner-friendly · Real examples throughout

[![Level](https://img.shields.io/badge/Level-Beginner_friendly-brightgreen)](https://github.com/irshadvaza/irshadvaza.tech/blob/main/learning-guides/ai-architect-guide)
[![Prerequisite](https://img.shields.io/badge/Prerequisite-Transformers_Guide-blue)](./transformers.md)
[![Architectures](https://img.shields.io/badge/Covers-RAG%20%7C%20Agents%20%7C%20MoE%20%7C%20Mamba%20%7C%20Jamba-purple)](https://github.com/irshadvaza/irshadvaza.tech)

---

## Prerequisites

This guide builds directly on the [Transformers guide](./transformers.md). Before reading this, make sure you understand:
- What a Transformer is and how self-attention works
- Why LSTM was replaced (sequential vs parallel processing)
- What "token", "embedding", and "context window" mean

If those feel solid, continue. If not, read the Transformers guide first.

---

## The Evolution Map

```
2017        2019        2020        2021        2022        2023        2024
  │           │           │           │           │           │           │
TRANSFORMER  GPT-2      GPT-3       RAG         AGENTS      MoE (MoE)   MAMBA
  │           │           │           │           │         Mixtral       │
Reads all   Generates   Scale hits  External    AI that     Only some    State
words at    text        context     knowledge   takes       experts      space
once        well        limits →    injected    actions     activate     model
            │           problems    │           │           │            │
            └────────── Each layer──┘           └───────────┘            │
                        costs same                                      MAMBA 2
                        for all tokens                                   │
                                                                        JAMBA
                                                              (Mamba + Transformer)
```

The Transformer was revolutionary — but as models got bigger and tasks got harder, three new problems emerged:

1. **Knowledge limit** — The model only knows what was in its training data. Stale facts, no private data.
2. **Passivity** — The model answers questions but can't take actions in the real world.
3. **Cost at scale** — Every token costs the same compute, even simple ones. Wasteful.
4. **Memory limit** — The quadratic cost of attention makes very long contexts expensive.

Each architecture in this guide was invented to solve one or more of these problems.

---

## Table of Contents

1. [RAG — Retrieval-Augmented Generation](#1-rag--retrieval-augmented-generation)
2. [Agents — AI That Takes Actions](#2-agents--ai-that-takes-actions)
3. [MoE — Mixture of Experts](#3-moe--mixture-of-experts)
4. [Mamba — The State Space Model](#4-mamba--the-state-space-model)
5. [Mamba 2 — What Changed](#5-mamba-2--what-changed)
6. [Jamba — The Hybrid](#6-jamba--the-hybrid)
7. [Falcon H1 — Where It All Comes Together](#7-falcon-h1--where-it-all-comes-together)
8. [Architecture Comparison — Side by Side](#8-architecture-comparison--side-by-side)
9. [Timeline — The Full Story](#9-timeline--the-full-story)
10. [Real-World Examples](#10-real-world-examples)
11. [Advantages & Disadvantages](#11-advantages--disadvantages)
12. [Summary — One-Page Cheat Sheet](#12-summary--one-page-cheat-sheet)
13. [Interview Q&A](#13-interview-qa)

---

## 1. RAG — Retrieval-Augmented Generation

### What is RAG? — One sentence

> **RAG is a technique that gives an AI model access to external documents at the moment it answers a question, so it is not limited to what it memorised during training.**

### Where did it come from? — The origin story

**The year:** 2020. **The problem:** GPT-3 just came out, and it was impressive — but it had a critical flaw.

Imagine hiring an expert consultant. This consultant read every book and article in the world — but only up until 2021. Now it is 2025. You ask: "What is the current price of oil?" The consultant has no idea. You ask: "What does our internal policy document say about refund procedures?" The consultant has never seen it.

That was the GPT-3 problem. Brilliant on general knowledge. Blind on anything recent, private, or specific.

**Lewis et al. (Facebook AI Research, 2020)** published the paper *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*. Their idea: instead of trying to memorise everything during training, let the model **look things up** at the moment of answering.

The name breaks down perfectly:
- **Retrieval** — go fetch relevant documents
- **Augmented** — add them to the model's input
- **Generation** — now generate your answer with that extra context

### How RAG works — step by step

```
User question: "What is our company's refund policy for SaaS subscriptions?"
                                │
                                ▼
                    STEP 1: EMBED THE QUESTION
                    Convert the question into a vector
                    [0.23, -0.11, 0.87, ...]  ← "refund policy" in vector space
                                │
                                ▼
                    STEP 2: SEARCH THE VECTOR DATABASE
                    Find documents with similar vectors
                    ┌─────────────────────────────────────┐
                    │  Document store (your private data): │
                    │  - policy-2024.pdf                  │
                    │  - employee-handbook.docx            │
                    │  - customer-faq.md                  │
                    └─────────────────────────────────────┘
                    Result: "policy-2024.pdf, section 3.2"
                    similarity score: 0.94
                                │
                                ▼
                    STEP 3: RETRIEVE THE CHUNK
                    "3.2 SaaS Subscription Refunds:
                     Customers may request a full refund
                     within 30 days of purchase..."
                                │
                                ▼
                    STEP 4: AUGMENT THE PROMPT
                    New prompt sent to the LLM:
                    ┌──────────────────────────────────────────────┐
                    │  Context: [retrieved policy text here]       │
                    │  Question: What is our refund policy for     │
                    │            SaaS subscriptions?               │
                    │  Answer based only on the context above.     │
                    └──────────────────────────────────────────────┘
                                │
                                ▼
                    STEP 5: GENERATE THE ANSWER
                    "Based on section 3.2 of the policy document,
                     customers are entitled to a full refund
                     within 30 days of purchase..."
```

### Simple analogy

**Without RAG:** The model is like a student who memorised everything before an open-book exam — but left all their books at home. They can only answer from memory.

**With RAG:** The student has their books on the desk. They read the question, flip to the right chapter, and answer using both memory and the book. Much more accurate.

### Why it was a breakthrough

| Problem before RAG | RAG solution |
|---|---|
| Model knowledge is frozen at training cutoff | Retrieve fresh documents at query time |
| Can't access private/internal data | Index your own documents in the vector store |
| Hallucination on specific facts | Ground the answer in retrieved source text |
| Must retrain to add new knowledge | Just add documents to the vector store |

### RAG in Falcon LLM — concrete example

**SmartSQL** (referenced in the transformers guide) uses RAG to:
1. Store your database schema in a vector database
2. When you ask a natural language question, retrieve the relevant table definitions
3. Pass those definitions to the LLM with the question
4. The LLM generates a SQL query grounded in your actual schema

Cost: ~$1.52/month. No schema retraining. This is RAG.

### RAG vs fine-tuning — which to use?

```
Use RAG when:
  ✓ Your knowledge changes frequently (news, prices, policies)
  ✓ You need to cite sources
  ✓ You have private/proprietary documents
  ✓ You want to add knowledge without retraining

Use Fine-tuning when:
  ✓ You want the model to behave differently (new tone, format, style)
  ✓ You want to teach a skill (e.g. write SQL in a specific dialect)
  ✓ The knowledge is stable and won't change
  ✓ You want faster inference (smaller, specialised model)
```

---

## 2. Agents — AI That Takes Actions

### What is an Agent? — One sentence

> **An Agent is an AI model that doesn't just answer questions — it decides what to do, uses tools to do it, observes the results, and repeats until the task is complete.**

### Where did it come from? — The origin story

**The year:** 2022–2023. **The problem:** GPT-3 was amazing at generating text, but it was fundamentally passive.

You could ask it: "Book me a flight to Dubai next Tuesday." It would write out instructions. But it couldn't actually open the flight booking website, search for flights, select one, and complete the purchase. It was a very smart advisor who couldn't pick up a phone.

The core insight, formalised by several research papers including *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022), was: **what if the model could use tools?**

What if the model could:
- Search the web
- Run code
- Read and write files
- Call APIs
- Control a browser
- Query a database

And then use the results of those actions to decide its next step?

That is an agent.

### How an Agent works — step by step

The core loop is called **ReAct** (Reason + Act):

```
User: "Research the top 3 competitors to our product and
       create a summary report in our Google Drive"

                    AGENT LOOP BEGINS
                           │
                    ┌──────▼───────┐
                    │   THOUGHT    │  "I need to search for competitors first"
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    ACTION    │  web_search("top competitors to [product]")
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ OBSERVATION  │  Returns: "Company A, Company B, Company C..."
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   THOUGHT    │  "Now I need details on each. Search them."
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    ACTION    │  web_search("Company A features pricing 2025")
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ OBSERVATION  │  Returns competitor details
                    └──────┬───────┘
                           │
               [Repeat for Company B and C]
                           │
                    ┌──────▼───────┐
                    │   THOUGHT    │  "I have enough info. Write the report."
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    ACTION    │  create_google_doc("Competitor Analysis")
                    │              │  write_content(summary_text)
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ OBSERVATION  │  "Document created: [link]"
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   THOUGHT    │  "Task complete. Report the link to the user."
                    └──────────────┘

User receives: "I've created the report here: [Google Drive link]"
```

### Simple analogy

**A non-agent LLM** is like a brilliant advisor in a meeting room. You describe the problem, they give you a great plan. Then you have to go execute it yourself.

**An agent** is like hiring that brilliant advisor as a full employee. They plan AND execute — they make the calls, write the emails, run the code, update the spreadsheet, and report back to you when done.

### The tools an agent can use

```
┌──────────────────────────────────────────────────────────────┐
│                         AGENT TOOLS                          │
├─────────────────┬────────────────────────────────────────────┤
│ web_search      │ Look up current information online         │
│ code_execution  │ Write and run Python, SQL, JavaScript      │
│ file_read/write │ Read PDFs, create documents, edit files    │
│ api_call        │ Talk to any REST API (Slack, Salesforce...) │
│ browser_control │ Navigate websites, click, fill forms       │
│ memory          │ Store and recall information across steps  │
│ sub_agent       │ Spin up another agent to do a subtask      │
└─────────────────┴────────────────────────────────────────────┘
```

### Multi-agent systems

The most powerful setups use **multiple agents working together**:

```
ORCHESTRATOR AGENT  ← receives the overall task
      │
      ├── RESEARCH AGENT   ← searches web, reads papers
      │
      ├── CODING AGENT     ← writes and runs code
      │
      ├── WRITING AGENT    ← composes the final report
      │
      └── QA AGENT         ← reviews output for errors
```

Each sub-agent specialises. The orchestrator coordinates. This is how modern AI systems like GitHub Copilot Workspace and Devin work.

### Why agents matter for Falcon LLM

Falcon H1 (TII's 2025 model) was specifically designed with agentic use cases in mind — with a longer context window and hybrid architecture optimised for multi-step reasoning and tool use, not just single-turn question answering.

---

## 3. MoE — Mixture of Experts

### What is MoE? — One sentence

> **MoE is an architecture where the model is divided into many specialised sub-networks ("experts"), and for each token, only a few of them activate — making the model far larger in capacity but not much more expensive to run.**

### Where did it come from? — The origin story

**The year:** 1991 (the idea), 2022–2023 (it became dominant). **The problem:** we wanted bigger models, but bigger models cost more to run.

By 2022, GPT-3 had 175 billion parameters. Getting to a trillion parameters would cost 6× more to run every single inference. That is not scalable.

**The old insight, newly powerful:** In 1991, Jacobs and Jordan proposed "Mixture of Experts" — the idea that a network could be divided into specialists, with a "gating network" routing each input to the right specialist. You get the combined capacity of all experts, but only pay for a few per input.

For decades, this idea was too hard to train reliably at scale. Then **Google** (in the 2021 paper *"Switch Transformers"*) and **Mistral AI** (in 2023, with Mixtral 8×7B) figured out how to make it work.

The result: **Mixtral 8×7B has the capacity of a ~47B parameter model, but runs with the compute cost of a ~13B model.**

### How MoE works — step by step

```
Standard Transformer (what you know):
  Token → Attention → Feed-Forward Network (ALL parameters activate)
  Cost:   100 operations for 100B parameters

MoE Transformer:
  Token → Attention → ROUTER → picks 2 of 8 experts → those 2 activate
                       │
                       ├── Expert 1: specialised in grammar/syntax
                       ├── Expert 2: specialised in factual recall
                       ├── Expert 3: specialised in code
                       ├── Expert 4: specialised in reasoning
                       ├── Expert 5: specialised in Arabic text
                       ├── Expert 6: specialised in scientific text
                       ├── Expert 7: specialised in conversation
                       └── Expert 8: specialised in instructions

  Cost:   25 operations (only 2/8 experts fire = 25% of the compute)
  But capacity: access to ALL 8 experts' knowledge when needed
```

### Simple analogy

**Standard model:** A single doctor who knows everything about all medical fields. For every patient visit, she uses all of her 40 years of knowledge. Expensive. Time-consuming.

**MoE model:** A hospital with 8 specialist doctors — cardiologist, neurologist, paediatrician, etc. A triage nurse (the router) decides which 2 doctors are relevant for this patient and sends the patient to them. Most patients only see 2 doctors. The hospital has far more combined knowledge than any single doctor, but each patient visit is faster.

### The router — how does it choose?

```
Input token: "كيف تعمل هذه المعادلة؟"  (Arabic: "How does this equation work?")

Router outputs probabilities:
  Expert 1 (grammar):     0.05
  Expert 2 (factual):     0.08
  Expert 3 (code):        0.04
  Expert 4 (reasoning):   0.15
  Expert 5 (Arabic):      0.42  ← highest — selected!
  Expert 6 (science):     0.18  ← second highest — selected!
  Expert 7 (conversation): 0.05
  Expert 8 (instructions): 0.03

Selected: Expert 5 (Arabic text) + Expert 6 (scientific text)
```

The router is a small, simple neural network that learns during training which inputs go to which experts.

### Load balancing — a critical problem

Early MoE had a failure mode: the router would learn to always use the same 1–2 experts, and the rest would never train. 

**The fix:** add an **auxiliary loss** during training that penalises uneven routing — essentially punishing the model if Expert 5 handles 80% of tokens while Expert 3 handles 2%. This forces balanced training across all experts.

### MoE in Falcon LLM

Falcon H1 (2025) uses a MoE architecture. Instead of paying the full compute cost of a large dense model for every token, specific experts activate based on what the token requires — whether it's Arabic language processing, code generation, or scientific reasoning. This is why Falcon H1 achieves state-of-the-art performance at a fraction of the compute cost of equivalently-sized dense models.

---

## 4. Mamba — The State Space Model

### What is Mamba? — One sentence

> **Mamba is an architecture that replaces the attention mechanism entirely with a mathematical system that processes sequences in linear time — making it dramatically faster and more memory-efficient than transformers for long sequences.**

### Where did it come from? — The origin story

**The year:** 2023. **The problem:** Transformers are brilliant, but they have a fundamental mathematical flaw when sequences get long.

Recall from the transformers guide: attention computes relationships between **every pair of tokens**. For a sequence of N tokens, that is N × N computations. This is **quadratic complexity**.

```
Sequence of 1,000 tokens:   1,000 × 1,000 = 1,000,000 computations
Sequence of 10,000 tokens:  10,000 × 10,000 = 100,000,000 computations
Sequence of 100,000 tokens: 100,000 × 100,000 = 10,000,000,000 computations

That is a 10,000× increase in compute for a 100× increase in sequence length.
```

For short sequences (a paragraph), this is fine. For long sequences (an entire legal document, a full codebase, a 1-hour meeting transcript), it becomes prohibitively expensive.

**Albert Gu and Tri Dao** at Carnegie Mellon University (2023) asked: can we design a sequence model that processes information in **linear time** — where doubling the sequence length just doubles the compute, not quadruples it?

Their answer was **Mamba**, built on the foundation of **State Space Models (SSMs)**.

### State Space Models — the mathematical foundation

SSMs come from **control theory and signal processing** — fields that predate machine learning by decades. They were used to model physical systems: the position of a satellite, the output of a circuit, the velocity of a car.

The core idea: **compress everything you've seen so far into a fixed-size "state" vector, then update that state as each new input arrives.**

```
State Space Model — the three equations:

h(t) = A·h(t-1) + B·x(t)      ← state update
y(t) = C·h(t) + D·x(t)        ← output

Where:
  x(t)  = current input (new token)
  h(t)  = hidden state (everything learned so far, compressed)
  y(t)  = output
  A, B, C, D = learned matrices (like weights in a neural network)
```

**Simple analogy for the state:** Imagine a running average of a river's water level. You don't store every measurement ever taken — you keep a single number (the state) that summarises the past and update it as new measurements arrive.

That is what Mamba's hidden state does — it compresses the entire context (potentially millions of tokens) into a fixed-size vector.

### The key innovation — selective state spaces

Early SSMs had a flaw: A, B, C were fixed matrices — the same regardless of what the input was. This meant the model couldn't selectively remember some things and forget others.

**Mamba's breakthrough:** make A, B, C **input-dependent**. The model learns to:
- Strongly update the state when an important token arrives
- Barely update the state when an unimportant token arrives

```
Token: "The"    → state update factor: 0.02  (ignore mostly)
Token: "cat"    → state update factor: 0.89  (important — store in state)
Token: "sat"    → state update factor: 0.76  (important — update state)
Token: "on"     → state update factor: 0.03  (ignore mostly)
Token: "mat"    → state update factor: 0.91  (important — store in state)
```

This is **selective state spaces** — the model selectively decides what to remember and what to forget, just like human attention.

### Mamba vs Transformer — the head-to-head

```
                    TRANSFORMER                   MAMBA
                    ───────────                   ─────
Mechanism:          Self-attention                Selective SSM
Complexity:         O(N²) — quadratic            O(N) — linear
Memory:             Grows with context length     Fixed state size
Training:           Parallel (fast)              Parallel (fast, via parallel scan)
Inference:          All tokens at once           Recurrent (process one at a time)
Long sequences:     Expensive                    Cheap
Short sequences:    Fast                         Slightly slower than transformers
Best for:           Short-medium contexts         Very long sequences
                    (under ~32K tokens)           (100K+ tokens)
```

### How Mamba processes a sequence — step by step

```
Input: "The cat sat on the mat"
         │   │   │   │   │   │
         ▼   ▼   ▼   ▼   ▼   ▼

Step 1: "The" arrives → state: [0.02, 0.00, 0.01, ...]
Step 2: "cat" arrives → state: [0.23, 0.87, 0.01, ...]  ← big update
Step 3: "sat" arrives → state: [0.21, 0.79, 0.76, ...]  ← big update
Step 4: "on"  arrives → state: [0.21, 0.78, 0.75, ...]  ← tiny update
Step 5: "mat" arrives → state: [0.19, 0.71, 0.68, 0.91, ...]  ← big update

Final state: a compressed summary of the whole sentence.
Output is generated from this state.

At every step, the model only stores the fixed-size state vector —
not all previous tokens. Memory is constant regardless of sequence length.
```

### Simple analogy — the Mamba vs Transformer difference

**Transformer:** Every student in a class passes their full notes to every other student for every question. Brilliant but expensive — the note-passing cost grows quadratically.

**Mamba:** There is one shared whiteboard (the state). Each student reads the whiteboard, updates it with their contribution, then passes to the next. The whiteboard is always the same size. Processing is fast and memory is fixed.

The tradeoff: with the whiteboard approach, old information can be overwritten. The transformer's approach preserves all information perfectly but at high cost.

---

## 5. Mamba 2 — What Changed

### What is Mamba 2? — One sentence

> **Mamba 2 is a refined version of Mamba that restructures the SSM equations to be mathematically equivalent to a restricted form of attention — making it faster to train and easier to integrate with transformer components.**

### Where did it come from? — The origin story

**The year:** 2024. **The problem:** Mamba (1) was excellent, but it was hard to train efficiently at very large scale because its core computation didn't map cleanly onto the matrix multiplications that modern GPUs are optimised for.

**Dao and Gu** (the same authors) revisited the mathematics. They showed that the SSM computation in Mamba could be rewritten as a **Structured State Space Duality (SSD)** — a form that is equivalent to a special restricted type of attention (called "semiseparable matrix attention").

This was important for two reasons:
1. The new form maps perfectly onto GPU hardware (tensor cores)
2. It proved theoretically that SSMs and attention are not completely different things — they exist on a spectrum

### What changed technically

```
Mamba 1 core operation:
  h(t) = A·h(t-1) + B·x(t)    ← sequential recurrence

Mamba 2 core operation:
  Uses a "chunk" approach:
  Split the sequence into chunks of ~64 tokens
  Within each chunk: use efficient matrix multiplication (like attention)
  Between chunks: use fast recurrence to pass the state

Result:
  - 2–8× faster training than Mamba 1
  - Same or better quality
  - Easier to combine with attention layers
```

### Simple analogy

Mamba 1 is like reading a book word by word and updating your mental notes after each word. Mamba 2 is like reading a paragraph at a time (using a quick matrix multiply within the paragraph), then updating your notes at the paragraph boundary. Faster, same result.

### Performance improvements

| Metric | Mamba 1 | Mamba 2 |
|---|---|---|
| Training throughput | Baseline | 2–8× faster |
| Model size tested | Up to 3B | Up to 8B+ |
| GPU utilisation | ~70% | ~90% |
| Combinability with attention | Difficult | Straightforward |

---

## 6. Jamba — The Hybrid

### What is Jamba? — One sentence

> **Jamba is a hybrid architecture from AI21 Labs that interleaves Transformer attention layers with Mamba SSM layers in the same model — getting the best of both worlds.**

### Where did it come from? — The origin story

**The year:** 2024. **The company:** AI21 Labs (Israel). **The problem:** neither pure transformers nor pure Mamba models were optimal.

- **Transformers** are excellent at precise recall — if you need to answer "what did the document say in section 3.2?", attention finds it perfectly. But they struggle with very long contexts due to O(N²) cost.
- **Mamba** handles very long sequences efficiently (O(N) cost), but pure SSMs are slightly weaker at precise selective recall tasks compared to attention.

AI21 Labs asked: **what if we combine them?**

Their insight: use attention layers for the "precise recall" and "global context" tasks, use Mamba layers for "efficient sequence compression" and "long-range memory". Alternate between them.

### How Jamba is structured

```
JAMBA ARCHITECTURE (simplified)

Token Input
    │
    ▼
┌─────────────────────────────────────────────┐
│  Layer 1: Mamba Layer (SSM)                 │  ← efficient sequence processing
├─────────────────────────────────────────────┤
│  Layer 2: Mamba Layer (SSM)                 │
├─────────────────────────────────────────────┤
│  Layer 3: Mamba Layer (SSM)                 │
├─────────────────────────────────────────────┤
│  Layer 4: Transformer Attention Layer       │  ← precise recall when needed
├─────────────────────────────────────────────┤
│  Layer 5: Mamba Layer (SSM)                 │
├─────────────────────────────────────────────┤
│  Layer 6: Mamba Layer (SSM)                 │
├─────────────────────────────────────────────┤
│  Layer 7: Mamba Layer (SSM)                 │
├─────────────────────────────────────────────┤
│  Layer 8: Transformer Attention Layer       │
└─────────────────────────────────────────────┘
                  + MoE Feed-Forward layers throughout
    │
    ▼
Output

Pattern: roughly 1 attention layer per 3 Mamba layers
```

### The ratio — why not 50/50?

Most information in a sequence is "background context" — the Mamba layers handle this efficiently. Only occasionally does the model need to "precisely look back" and retrieve something exact — the attention layers handle those moments.

Empirically, AI21 found that 1 attention layer per 3–4 Mamba layers hits the sweet spot:
- Enough attention for precise recall
- Enough Mamba for efficient long-context compression
- The MoE layers reduce per-token compute further

### Simple analogy

Imagine a research team reading a 1,000-page report:

- **Mamba layers** = a junior analyst who reads everything quickly and keeps running notes (the state). They won't remember every exact sentence, but they have a good overall understanding.
- **Attention layers** = a senior expert who occasionally steps in, looks back at the exact pages, and gives a precise answer.

Together, they're faster and more accurate than either alone.

### Jamba performance

Jamba-1.5 (AI21 Labs, 2024):
- **Context window:** 256K tokens (the equivalent of a full novel)
- **Speed:** 3× faster inference than comparable transformer-only models at long context
- **Memory:** Fits long contexts in smaller GPU memory
- **Quality:** Matches GPT-4 on many benchmarks

---

## 7. Falcon H1 — Where It All Comes Together

### What is Falcon H1?

> **Falcon H1 is TII's (Technology Innovation Institute, UAE) 2025 flagship model that combines a hybrid Mamba 2 + Transformer architecture with MoE — representing the convergence of everything in this guide.**

Falcon H1 is the direct successor to the Falcon 7B and 40B transformer models. It incorporates lessons from every architecture discussed:

```
FALCON H1 ARCHITECTURE

┌─────────────────────────────────────────────┐
│            FALCON H1 COMPONENTS             │
├─────────────────────────────────────────────┤
│ Base: Hybrid SSM + Transformer              │
│       (Mamba 2 layers + Attention layers)   │
├─────────────────────────────────────────────┤
│ Scale: Mixture of Experts (MoE)             │
│       (only some experts activate per token) │
├─────────────────────────────────────────────┤
│ Knowledge: Designed for RAG integration     │
│       (long context for document retrieval) │
├─────────────────────────────────────────────┤
│ Use: Agentic tasks                          │
│       (tool use, multi-step reasoning)      │
└─────────────────────────────────────────────┘
```

### Why this combination?

| Component | What it solves |
|---|---|
| Mamba 2 layers | Long-context efficiency (O(N) vs O(N²)) |
| Transformer attention | Precise recall and global context |
| MoE | Scale capacity without proportional cost |
| Long context window | Enables complex RAG and agent tasks |

Falcon H1 tiny models (0.5B–1.5B parameters) outperform models 3–5× their size on many benchmarks — because the hybrid architecture is fundamentally more efficient than pure transformers at the same parameter count.

---

## 8. Architecture Comparison — Side by Side

```
┌─────────────────┬────────────┬──────────┬────────────┬──────────┬──────────┐
│                 │TRANSFORMER │  MAMBA   │  MAMBA 2   │  JAMBA   │   MoE    │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Core mechanism  │ Attention  │ SSM      │ SSD        │ SSM +    │ Gated    │
│                 │ (O(N²))    │ (O(N))   │ (O(N))     │ Attention│ Experts  │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Long sequences  │ Expensive  │ Cheap    │ Cheap      │ Balanced │ Depends  │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Precise recall  │ Excellent  │ Good     │ Good       │ Excellent│ Depends  │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Training speed  │ Fast       │ Moderate │ Fast       │ Fast     │ Fast     │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Inference cost  │ Medium     │ Low      │ Low        │ Low-Med  │ Low      │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Memory usage    │ Grows      │ Fixed    │ Fixed      │ Balanced │ Large    │
│                 │ with N     │ state    │ state      │          │ but MoE  │
├─────────────────┼────────────┼──────────┼────────────┼──────────┼──────────┤
│ Example models  │ GPT-4      │ Mamba-3B │ Falcon H1  │ Jamba    │ Mixtral  │
│                 │ Falcon 7B  │          │            │ 1.5      │ Falcon H1│
└─────────────────┴────────────┴──────────┴────────────┴──────────┴──────────┘
```

### Which one to use?

```
I need to answer questions about private documents:
  → Use RAG (on top of any base model)

I need the AI to complete multi-step tasks automatically:
  → Use Agents

I need a massive model that's affordable to run:
  → Use MoE (Mixtral, Falcon H1)

I need to process very long documents (100K+ tokens):
  → Use Mamba or Jamba

I need the best balance of quality and efficiency:
  → Use Jamba or Falcon H1 (Mamba + Transformer + MoE hybrid)

I need a model for short-to-medium tasks, maximum quality:
  → Transformer is still excellent (GPT-4, Falcon classic)
```

---

## 9. Timeline — The Full Story

```
2017 ────────────────────────────────────────────────────────────── 2025
  │                                                                     │
  ●──────────────●────────●──────────●──────────●──────────●───────────●
2017            2020     2021        2022        2023      2024        2025
  │               │        │           │           │          │           │
TRANSFORMER     RAG     Switch      ReAct       MAMBA    MAMBA 2     FALCON H1
"Attention     (Facebook Transformers (Agents)  (Gu & Dao (Dao & Gu)  Hybrid:
Is All You     AI 2020) Google 2021  (Yao 2022) CMU 2023) CMU 2024)  Mamba2 +
Need"          External MoE at                  SSM:      Faster,    Attention
               knowledge scale                  O(N) cost GPU-opt    + MoE
               via RAG  proven                  replaces  Jamba      256K ctx
                                                attention (AI21)     Agentic
```

**Era summary:**

| Period | Architecture | Key advance |
|---|---|---|
| 2017 | Transformer | Parallel processing, attention, scales to billions of parameters |
| 2020 | RAG | Models can access external knowledge at inference time |
| 2021 | MoE (Switch Transformers) | Sparse activation — bigger capacity, same compute |
| 2022 | Agents / ReAct | Models can use tools and take actions in the world |
| 2023 | Mamba | Linear-time sequence processing, replaces attention for long contexts |
| 2024 | Mamba 2 / Jamba | Faster SSMs, hybrid Mamba+Transformer architectures proven |
| 2025 | Falcon H1 | Full convergence: SSM + Attention + MoE in one production model |

---

## 10. Real-World Examples

### Mixtral 8×7B (Mistral AI, 2023) — MoE in practice

- **Architecture:** 8 expert networks, 2 activate per token
- **Effective parameters:** ~13B active out of ~47B total
- **Performance:** Matches GPT-3.5 at a fraction of the inference cost
- **Open source:** Yes — downloadable and runnable locally
- **Impact:** Proved that open-source MoE could compete with closed proprietary models

### Jamba 1.5 (AI21 Labs, 2024) — The hybrid in practice

- **Architecture:** Mamba + Transformer + MoE
- **Context window:** 256,000 tokens (~512 pages of text)
- **Speed:** Processes a 100-page document 3× faster than GPT-4-Turbo
- **Use case:** Legal document analysis, long-form research synthesis, entire codebase understanding

### Claude (Anthropic) — Long context

- **Architecture:** Transformer (with research into SSM improvements)
- **Context window:** 200,000 tokens in Claude 3 models
- **Use case for long context:** Entire technical documentation, large codebases, book-length documents

### GitHub Copilot Workspace — Agents in practice

- **Architecture:** Agent system on top of GPT-4 / Claude
- **What it does:** Given a GitHub issue, it plans the solution, writes code changes across multiple files, runs tests, and creates a pull request — with minimal human intervention
- **The agent loop:** Reason about the issue → write code → run tests → observe results → fix errors → commit

### Perplexity AI — RAG in practice

- **Architecture:** LLM (transformer) + real-time web retrieval (RAG)
- **What it does:** Answers questions with up-to-date information, cites sources
- **Why it works:** Every answer retrieves fresh web content — it never goes stale
- **Why it doesn't hallucinate (much):** Answers are grounded in retrieved text, not pure memory

### Falcon H1 (TII Abu Dhabi, 2025) — Everything together

- **Architecture:** Mamba 2 + Transformer attention + MoE
- **Sizes:** 0.5B, 1.5B, 7B, 34B parameters
- **Languages:** Strong Arabic + English + multilingual
- **Key achievement:** The 1.5B model outperforms many 7B transformer models
- **Target:** Agentic tasks, long-document RAG, efficient deployment in UAE government and enterprise

---

## 11. Advantages & Disadvantages

### RAG

| Advantages | Disadvantages |
|---|---|
| Always up-to-date knowledge | Requires building and maintaining a vector database |
| Can use private/proprietary data | Quality depends on retrieval quality — garbage in, garbage out |
| Reduces hallucination on factual tasks | Extra latency from the retrieval step |
| No retraining needed | Complex to tune the retrieval system |
| Sources are citable and auditable | Chunking documents well is a real engineering challenge |

### Agents

| Advantages | Disadvantages |
|---|---|
| Can complete real-world multi-step tasks | Hard to predict or control — may take wrong actions |
| Can use any tool (web, code, files, APIs) | Error propagation — a wrong step early derails everything |
| Scales to complex workflows | Expensive — many LLM calls per task |
| Can self-correct by observing results | Safety concerns — agents can take irreversible actions |
| Reduces human effort | Harder to audit than a single LLM call |

### MoE

| Advantages | Disadvantages |
|---|---|
| Large model capacity at low compute cost | Much larger total parameter count (harder to store) |
| Experts can specialise in different domains | Routing can fail — some experts may not train well |
| Scales capacity without proportional cost | Requires careful load-balancing during training |
| Works well with transformer or SSM base | Communication overhead in distributed training |
| Proven in production (Mixtral, Falcon H1) | Less predictable than dense models in some edge cases |

### Mamba

| Advantages | Disadvantages |
|---|---|
| Linear-time complexity — O(N) | Slightly weaker than attention on precise recall tasks |
| Fixed memory regardless of context length | Less mature ecosystem than transformers |
| Excellent for 100K+ token sequences | Harder to fine-tune than transformers |
| Efficient inference (recurrent mode) | Parallel training requires specialised CUDA kernels |
| State-of-the-art for audio, genomics, time series | Less interpretable than attention (no attention maps) |

### Jamba (Hybrid)

| Advantages | Disadvantages |
|---|---|
| Best of both: efficiency + precise recall | More complex to train |
| Long context at low memory cost | Fewer open-source implementations |
| Proven at 256K token context | Ratio of attention:SSM layers requires tuning |
| Compatible with both transformer and SSM tools | Emergent from very recent research — fewer battle-tested deployments |

---

## 12. Summary — One-Page Cheat Sheet

```
THE FIVE ARCHITECTURES BEYOND TRANSFORMERS

┌─────┬─────────────────────────────────────────────────────────────────┐
│ RAG │ Retrieval-Augmented Generation                                  │
│     │ What: Fetch external documents at query time, inject into prompt │
│     │ Why: Transformers have stale knowledge + can't see private data  │
│     │ How: Embed → Search vector DB → Retrieve → Augment → Generate   │
│     │ Use when: Fresh knowledge, private docs, reduce hallucination    │
└─────┴─────────────────────────────────────────────────────────────────┘

┌────────┬──────────────────────────────────────────────────────────────┐
│ AGENTS │ AI that takes actions in the world                           │
│        │ What: LLM + tools, loops: Reason → Act → Observe → Repeat   │
│        │ Why: Passive LLMs can't execute, only advise                 │
│        │ How: ReAct loop + tool access (web, code, APIs, files)       │
│        │ Use when: Multi-step tasks, automation, complex workflows    │
└────────┴──────────────────────────────────────────────────────────────┘

┌─────┬─────────────────────────────────────────────────────────────────┐
│ MoE │ Mixture of Experts                                             │
│     │ What: N expert networks, router picks K of them per token      │
│     │ Why: Scale capacity without proportional compute cost          │
│     │ How: Router → Top-K experts activate → Outputs merged          │
│     │ Use when: Need very large model capacity at affordable cost    │
└─────┴─────────────────────────────────────────────────────────────────┘

┌───────┬───────────────────────────────────────────────────────────────┐
│ MAMBA │ State Space Model                                             │
│       │ What: Replaces attention with selective SSM recurrence        │
│       │ Why: Attention is O(N²), SSM is O(N) — linear in sequence len │
│       │ How: State h(t) = A·h(t-1) + B·x(t); selective gating       │
│       │ Use when: Very long sequences (100K+ tokens), low memory     │
└───────┴───────────────────────────────────────────────────────────────┘

┌───────┬───────────────────────────────────────────────────────────────┐
│ JAMBA │ Hybrid SSM + Transformer                                     │
│       │ What: Alternates Mamba layers with Transformer attention     │
│       │ Why: Neither alone is optimal — combine their strengths      │
│       │ How: ~3 Mamba layers per 1 Attention layer + MoE FFN         │
│       │ Use when: Long context + need precise recall                 │
└───────┴───────────────────────────────────────────────────────────────┘

THE EVOLUTION:
  Transformer (2017) → too expensive for long sequences
  + RAG (2020)        → adds fresh knowledge, no retraining
  + Agents (2022)     → adds action, not just words
  + MoE (2021–2023)   → more capacity, same cost
  + Mamba (2023)      → linear-time long sequences
  + Jamba (2024)      → best of SSM + Transformer
  → Falcon H1 (2025)  → SSM + Attention + MoE: all combined

KEY NUMBERS:
  Transformer attention: O(N²)
  Mamba SSM:             O(N)
  MoE activation ratio:  top-2 of 8 experts = 25% compute per token
  Jamba context:         256,000 tokens
  Falcon H1 1.5B:        beats most 7B transformer models
```

---

## 13. Interview Q&A

### "What is RAG and why is it used instead of fine-tuning?"

RAG (Retrieval-Augmented Generation) is a technique where relevant documents are retrieved from an external database at query time and injected into the prompt, so the model can generate answers grounded in that external content. Fine-tuning, by contrast, changes the model's weights to encode new knowledge permanently. RAG is preferred when knowledge changes frequently (news, prices, policies), when you need to cite sources, or when the knowledge base is too large or private to encode into model weights. Fine-tuning is preferred when you want to change the model's behaviour or style, not just add knowledge.

### "What is a Mixture of Experts (MoE) model?"

A Mixture of Experts model divides the feed-forward layers of a transformer into N separate "expert" sub-networks, with a learned router that selects only K of them (typically 1–2) for each token. This means the model has the combined capacity of all N experts — much larger than a dense model — but only pays the compute cost of K experts per token. Mixtral 8×7B, for example, has the total capacity of a 47B parameter model but runs with approximately 13B parameters of compute per token. The challenge is ensuring balanced utilisation across experts during training.

### "What is Mamba and how is it different from a Transformer?"

Mamba is a sequence model based on Selective State Spaces (SSMs) rather than attention. The core difference is computational complexity: attention computes relationships between every pair of tokens, giving O(N²) complexity with sequence length N. Mamba compresses all previous context into a fixed-size hidden state vector that is updated as each new token arrives, giving O(N) linear complexity. This makes Mamba dramatically more efficient for long sequences (100K+ tokens), but it trades off some of the precise recall capability that attention provides by directly looking back at any past token.

### "What is a Jamba architecture and why would you use it?"

Jamba is a hybrid architecture that interleaves Mamba SSM layers with Transformer attention layers in the same model (typically 3–4 Mamba layers for every 1 attention layer), combined with MoE feed-forward networks. The motivation is that pure Mamba is efficient but slightly weaker on precise recall tasks, while pure Transformers are excellent at recall but expensive for long contexts. Jamba achieves both: the Mamba layers handle long-range sequence compression efficiently, while the attention layers provide precise recall when needed. Jamba 1.5 supports 256K token contexts at 3× the inference speed of comparable transformer-only models.

### "What is an AI agent and how does it differ from a standard LLM?"

A standard LLM receives a prompt and generates a response — it is stateless and passive. An AI agent extends this with a loop: Reason (think about what to do) → Act (use a tool: web search, code execution, API call, file operation) → Observe (see the result) → Reason again. This loop continues until the task is complete. Agents can make multiple LLM calls, use external tools, maintain state across steps, and produce real-world outputs (files created, emails sent, code committed). The tradeoff is higher cost, harder auditability, and the possibility of error propagation — a wrong decision early in the loop can derail subsequent steps.

### "What is the difference between Mamba 1 and Mamba 2?"

Mamba 1 uses a sequential recurrence computation: h(t) = A·h(t-1) + B·x(t). This is conceptually clean but doesn't map efficiently onto the matrix multiplication units (tensor cores) that modern GPUs are optimised for. Mamba 2 restructures this computation as a "Structured State Space Duality" (SSD), showing it is mathematically equivalent to a restricted form of attention. This allows the computation to use efficient chunked matrix multiplications — processing ~64 tokens at a time within a chunk using a matmul, then passing the state between chunks via fast recurrence. The result is 2–8× faster training, better GPU utilisation, and easier integration with transformer attention layers in hybrid architectures.

---

## Resources

- [RAG paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401)
- [ReAct paper: Synergizing Reasoning and Acting in Language Models (Yao et al. 2022)](https://arxiv.org/abs/2210.03629)
- [Switch Transformers — MoE at scale (Fedus et al. 2021)](https://arxiv.org/abs/2101.03961)
- [Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao 2023)](https://arxiv.org/abs/2312.00752)
- [Mamba 2: Transformers are SSMs (Dao & Gu 2024)](https://arxiv.org/abs/2405.21060)
- [Jamba: A Hybrid Transformer-Mamba Language Model (AI21 Labs 2024)](https://arxiv.org/abs/2403.19887)
- [Falcon H1 — TII Abu Dhabi (2025)](https://falconllm.tii.ae/)
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) (prerequisite reading)
- [Lilian Weng's blog on LLM-powered agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

## What's Next?

The evolution continues. Current research frontiers (2025):

- **Test-time compute scaling** — models that think longer for harder problems (OpenAI o1, DeepSeek R1)
- **World models** — models that build internal simulations of the world, not just language
- **Neuromorphic hardware** — chips designed for SSM-style recurrent computation
- **Multi-modal SSMs** — applying Mamba to video, audio, and sensor data at scale

The architectures in this guide are the foundation. Every model being built today — including the next version of Falcon — is built on some combination of these ideas.

---

*Learning Guides — AI Foundations Series by [Irshad Vaza](https://irshadvaza.tech)*  
*Contact: aiandsmartdata@gmail.com*
