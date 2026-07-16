# Domain 4: Implement Generative AI Quality Assurance and Observability (10–15%)

⬅ [Previous: Domain 3](./03-Domain3-GenAIOps-Infrastructure.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 5 – Optimize GenAI Performance](./05-Domain5-Optimize-GenAI-Performance.md)

---

## 🧭 Domain Overview

Deploying a GenAI app is easy; **knowing it's actually good, safe, and affordable** is the hard part. This domain covers **evaluation** (is the output high quality and safe?) and **observability** (can I see what's happening in production — latency, cost, errors?).

Two sub-topics:
1. Configure evaluation and validation for generative AI applications and agents
2. Implement observability for generative AI applications and agents

---

## 1️⃣ Configure Evaluation and Validation for Generative AI Applications and Agents

### 🔑 Plain-English Explanation

You can't unit-test a GenAI response the way you'd test `add(2,2) == 4`. Instead, you build **evaluation pipelines** that score responses against quality and safety dimensions using a **test dataset** and either built-in or custom metrics.

### 📋 Core Quality Metrics — Know These Cold

| Metric | Question It Answers |
|---|---|
| **Groundedness** | Is the response factually supported by the provided context/retrieved documents (i.e., not hallucinated)? |
| **Relevance** | Does the response actually address the user's question? |
| **Coherence** | Is the response logically structured and easy to follow? |
| **Fluency** | Is the language grammatically correct and natural? |

### 🛡️ Risk & Safety Evaluations

| Category | Checks For |
|---|---|
| **Hateful/unfair content** | Discriminatory or biased language |
| **Sexual content** | Inappropriate sexual material |
| **Violent content** | Graphic violence, incitement |
| **Self-harm content** | Content promoting self-harm |
| **Jailbreak / prompt injection** | Attempts to bypass system instructions |

### 🏗️ Real-World Artifact — Building a Test Dataset + Evaluation Run

```jsonl
// eval_dataset.jsonl — each line = one test case
{"question": "What is Contoso's return policy?", "context": "Contoso allows returns within 30 days with receipt.", "ground_truth": "Returns are accepted within 30 days with a receipt."}
{"question": "Can I return an item after 60 days?", "context": "Contoso allows returns within 30 days with receipt.", "ground_truth": "No, returns are only accepted within 30 days."}
```

```python
from azure.ai.evaluation import evaluate, GroundednessEvaluator, RelevanceEvaluator, CoherenceEvaluator

result = evaluate(
    data="eval_dataset.jsonl",
    evaluators={
        "groundedness": GroundednessEvaluator(model_config),
        "relevance": RelevanceEvaluator(model_config),
        "coherence": CoherenceEvaluator(model_config),
    },
    evaluator_config={"default": {"column_mapping": {
        "query": "${data.question}",
        "context": "${data.context}",
        "response": "${target.response}"
    }}}
)
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Groundedness = catches | **Hallucinations** — the #1 GenAI-specific quality concern |
| Test dataset needs | Representative real-world queries + context + (ideally) ground truth answers |
| Automated evaluation workflows | Wired into CI/CD — run evaluation on every prompt/model change before promoting |
| Built-in vs. custom metrics | Use built-ins (groundedness, relevance, etc.) where possible; write custom metrics for domain-specific quality bars |

---

### ❓ Practice Questions — Evaluation & Validation

**Q1.** Your RAG-based support bot sometimes generates confident-sounding answers that aren't actually supported by the retrieved documents. Which evaluation metric is specifically designed to catch this?

A) Fluency
B) Coherence
C) Groundedness
D) Latency

✅ **Answer: C) Groundedness**

💡 **Explanation:** **Groundedness** measures whether a response is factually supported by the provided context — directly catching **hallucinations**, which is exactly the "confident but unsupported" failure mode described. Fluency and coherence assess language quality/structure, not factual accuracy against source material.

---

**Q2.** You want to make sure that before any updated prompt or fine-tuned model reaches production, it automatically passes a minimum quality bar (groundedness ≥ 4/5, no safety violations) without a human manually running checks each time. What should you implement?

A) Manual QA review only, on a best-effort basis
B) An automated evaluation workflow integrated into the CI/CD pipeline that gates promotion on metric thresholds
C) Deploy directly to production and monitor for complaints
D) Only run evaluations once per quarter

✅ **Answer: B) An automated evaluation workflow integrated into the CI/CD pipeline that gates promotion on metric thresholds**

💡 **Explanation:** The skills outline calls for **"automated evaluation workflows … by using built-in and custom evaluation metrics."** Wiring evaluation into CI/CD as a **quality gate** (fail the pipeline if groundedness/safety thresholds aren't met) is the GenAIOps equivalent of automated testing — catching regressions before they reach users, not after.

---

**Q3.** Which type of evaluation would specifically detect that your chatbot could be manipulated via a crafted user message into ignoring its system instructions and revealing internal configuration?

A) Fluency evaluation
B) Jailbreak / prompt injection risk and safety evaluation
C) Coherence evaluation
D) Relevance evaluation

✅ **Answer: B) Jailbreak / prompt injection risk and safety evaluation**

💡 **Explanation:** **Jailbreak/prompt injection evaluations** specifically test whether adversarial inputs can bypass system-level instructions — a distinct risk-and-safety category from output-quality metrics like fluency, coherence, or relevance.

---

## 2️⃣ Implement Observability for Generative AI Applications and Agents

### 🔑 Plain-English Explanation

Once live, you need eyes on **performance**, **cost**, and **debuggability** — this is where Foundry's continuous monitoring integrates with **Azure Monitor / Application Insights**.

| Concept | What it tracks |
|---|---|
| **Continuous monitoring in Foundry** | Ongoing tracking of quality + safety metrics on live traffic (sampled), not just at build time |
| **Performance metrics** | Latency (time-to-first-token, total response time), throughput (requests/sec), response times under load |
| **Cost metrics** | **Token consumption** (input + output tokens), which directly drives spend; resource utilization |
| **Logging, tracing, debugging** | Detailed traces of each request — retrieved documents, prompt sent, tokens used, model response — for root-cause analysis |

### 🏗️ Real-World Artifact — Tracing Configuration + Sample Trace

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(connection_string=app_insights_connection_string)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("rag_chat_completion") as span:
    span.set_attribute("gen_ai.request.model", "gpt-4o-ptu-prod")
    retrieved_docs = retrieve(query)
    span.set_attribute("retrieval.doc_count", len(retrieved_docs))
    response = generate(query, retrieved_docs)
    span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
    span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
```

```kusto
// Application Insights / Log Analytics — cost & latency query
customEvents
| where name == "rag_chat_completion"
| summarize
    avg_latency_ms = avg(todouble(customDimensions["duration_ms"])),
    total_input_tokens = sum(toint(customDimensions["gen_ai.usage.input_tokens"])),
    total_output_tokens = sum(toint(customDimensions["gen_ai.usage.output_tokens"]))
  by bin(timestamp, 1h)
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Token consumption matters because | It is the **primary cost driver** for foundation model usage (pay-per-token pricing) |
| Time-to-first-token (TTFT) | Key latency metric for perceived responsiveness in streaming chat UIs |
| Where traces land | Azure Monitor / Application Insights, queryable via Kusto (KQL) |
| Why detailed tracing matters | Lets you reconstruct *exactly* what context/prompt/response caused a bad output — essential for debugging hallucinations or safety incidents |

---

### ❓ Practice Questions — Observability

**Q4.** Your finance team notices GenAI-related Azure spend tripled last month with no increase in user volume. Which metric should you investigate first to understand the root cause?

A) Coherence score trend
B) Token consumption per request over time
C) Number of Git commits to the prompts repository
D) Compute cluster idle time

✅ **Answer: B) Token consumption per request over time**

💡 **Explanation:** Foundation model billing is **token-based**, so a cost spike with flat user volume points directly to increased **tokens per request** — perhaps prompts grew longer, retrieval is returning more/larger chunks, or responses have gotten verbose. Tracking token consumption is explicitly named in the skills outline under cost metrics.

---

**Q5.** A user reports that your chatbot gave a nonsensical answer yesterday at 3:14 PM. You need to determine exactly what context was retrieved and what prompt was sent to the model at that moment to diagnose the issue. What capability should you rely on?

A) Aggregate monthly usage dashboards only
B) Detailed logging and tracing that captures per-request prompt, retrieved context, and response
C) Ask the user to describe what they remember
D) Re-run the current prompt today and assume it reproduces the same issue

✅ **Answer: B) Detailed logging and tracing that captures per-request prompt, retrieved context, and response**

💡 **Explanation:** Root-causing a specific bad response requires **request-level tracing** — capturing the exact prompt, retrieved documents, and model output for that specific timestamp/request ID. Aggregate dashboards show trends, not the specific data needed for this kind of production troubleshooting.

---

**Q6.** Which two metrics together best characterize the "performance" (not quality, not cost) of a generative AI application in production? (Choose 2)

A) Groundedness score
B) Latency (response time)
C) Throughput (requests handled per second)
D) Fluency score

✅ **Answer: B) Latency (response time), and C) Throughput (requests handled per second)**

💡 **Explanation:** **Latency and throughput** are the classic system-performance metrics — how fast and how much. Groundedness and fluency are **quality** metrics (Domain 4, sub-topic 1), a different concern from raw system performance, even though both fall under the same domain.

---

## 🧠 Domain 4 Quick-Recall Cheat Sheet

- **Quality metrics**: Groundedness (hallucination check), Relevance, Coherence, Fluency
- **Safety evaluations**: hateful/unfair, sexual, violent, self-harm content, jailbreak/prompt injection
- **Evaluation workflow**: test dataset → run evaluators → gate CI/CD promotion on thresholds
- **Observability**: performance (latency, throughput) + cost (**token consumption**) + detailed tracing for debugging
- **Continuous monitoring** in Foundry watches live traffic, not just pre-deployment tests

---

⬅ [Previous: Domain 3](./03-Domain3-GenAIOps-Infrastructure.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 5 – Optimize GenAI Performance](./05-Domain5-Optimize-GenAI-Performance.md)
