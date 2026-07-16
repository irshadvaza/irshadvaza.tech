# Domain 5: Optimize Generative AI Systems and Model Performance (10–15%)

⬅ [Previous: Domain 4](./04-Domain4-Quality-Assurance-Observability.md) | ⬅ [Back to README](./README.md)

---

## 🧭 Domain Overview

The final domain assumes your GenAI system is already deployed and monitored (Domains 3–4) — now you make it **better**: more accurate retrieval, smarter search, and customized models via fine-tuning.

Two sub-topics:
1. Optimize retrieval-augmented generation (RAG) performance and accuracy
2. Implement advanced fine-tuning and model customization

---

## 1️⃣ Optimize Retrieval-Augmented Generation (RAG) Performance and Accuracy

### 🔑 Plain-English Explanation

RAG = **retrieve relevant documents → stuff them into the prompt → generate a grounded answer.** Most "my chatbot gives bad answers" problems are actually **retrieval** problems, not model problems. This sub-topic is about tuning the retrieval half of the pipeline.

| Lever | What It Controls |
|---|---|
| **Similarity threshold** | Minimum relevance score for a chunk to be included — too low = noisy/irrelevant context; too high = misses relevant info |
| **Chunk size** | How documents are split before embedding — too large = diluted/imprecise matches; too small = loses context |
| **Retrieval strategy** | How many chunks (top-k) to retrieve, re-ranking, query rewriting |
| **Embedding model selection** | General-purpose vs. domain-fine-tuned embeddings for specialized vocabulary (legal, medical, etc.) |
| **Hybrid search** | Combines **semantic (vector) search** + **keyword (BM25/lexical) search** for best of both worlds |
| **Evaluation of RAG quality** | Relevance metrics + A/B testing between retrieval configurations |

### 🏗️ Real-World Artifact — Tuning Chunking + Hybrid Search

```python
# Chunking configuration — balancing context vs. precision
from azure.search.documents.indexes.models import SplitSkill

split_skill = SplitSkill(
    text_split_mode="pages",
    maximum_page_length=512,     # tokens per chunk — tune based on eval results
    page_overlap_length=64       # overlap preserves context across chunk boundaries
)
```

```python
# Hybrid search query — semantic + keyword combined
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

results = search_client.search(
    search_text=user_query,                      # keyword/BM25 component
    vector_queries=[VectorizedQuery(
        vector=query_embedding, k_nearest_neighbors=5, fields="content_vector"
    )],                                            # semantic/vector component
    query_type="semantic",                        # enables re-ranking layer
    semantic_configuration_name="default"
)
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Chunk too large | Embeddings become "averaged"/diluted → lower retrieval precision |
| Chunk too small | Loses surrounding context → retrieved snippet is ambiguous |
| Chunk overlap | Prevents relevant info from being split across a hard chunk boundary |
| Hybrid search benefit | Vector search catches semantic meaning; keyword search catches exact terms (IDs, codes, acronyms) that embeddings sometimes miss |
| Domain-specific embeddings | Fine-tuning/selecting a specialized embedding model improves retrieval for jargon-heavy domains |
| Evaluating RAG changes | Use relevance metrics (Domain 4) + **A/B testing** between old vs. new retrieval configuration |

---

### ❓ Practice Questions — RAG Optimization

**Q1.** Your RAG chatbot for a legal document repository frequently fails to retrieve the correct clause when users search using exact legal citation numbers (e.g., "Section 12.4.1"), even though semantic search generally works well for conceptual questions. What should you implement to fix this specific gap?

A) Increase the chunk size further
B) Implement hybrid search combining semantic (vector) and keyword-based retrieval
C) Switch to a larger generative model
D) Lower the similarity threshold to zero

✅ **Answer: B) Implement hybrid search combining semantic (vector) and keyword-based retrieval**

💡 **Explanation:** Exact identifiers like citation numbers are often **poorly captured by embeddings** (which encode semantic meaning, not exact tokens) but are easily matched by **keyword/lexical search**. **Hybrid search** combines both, catching cases like this while retaining strong semantic matching for conceptual queries. Changing the generative model or chunk size doesn't address a retrieval-matching problem.

---

**Q2.** After reviewing evaluation results, you find that many retrieved chunks are only tangentially related to user questions, diluting the context sent to the model and lowering groundedness scores. Your current chunk size is 2,000 tokens. What should you try first?

A) Increase chunk size to 4,000 tokens
B) Reduce chunk size to improve retrieval precision, and re-evaluate
C) Disable retrieval entirely and rely on the model's parametric knowledge
D) Increase the number of retrieved chunks (top-k) without changing chunk size

✅ **Answer: B) Reduce chunk size to improve retrieval precision, and re-evaluate**

💡 **Explanation:** Large chunks tend to blend multiple topics into a single embedding, **diluting** relevance — smaller, more focused chunks generally improve retrieval precision (at the cost of potentially losing broader context, which is why **overlap** and **evaluation-driven tuning** matter). The skills outline explicitly names "tuning... chunk sizes" as an optimization lever, and this scenario's symptom (tangentially related chunks) is the classic signature of chunks being too large.

---

**Q3.** You changed your embedding model from a general-purpose model to one fine-tuned on your industry's domain-specific vocabulary. How should you validate whether this actually improved your RAG system before rolling it out fully?

A) Assume it's better since it's domain-specific
B) Run an A/B test comparing relevance/groundedness metrics between the old and new embedding model on the same evaluation dataset
C) Deploy directly to 100% of production traffic immediately
D) Skip evaluation since embedding changes don't affect output quality

✅ **Answer: B) Run an A/B test comparing relevance/groundedness metrics between the old and new embedding model on the same evaluation dataset**

💡 **Explanation:** The skills outline explicitly calls for evaluating RAG performance "by using relevance metrics and **A/B testing frameworks**." Domain-specific embeddings usually help, but "usually" isn't good enough for a production change — measure it against a held-out evaluation set before full rollout.

---

## 2️⃣ Implement Advanced Fine-Tuning and Model Customization

### 🔑 Plain-English Explanation

When prompt engineering and RAG aren't enough (e.g., you need a very specific output format, tone, or specialized reasoning pattern baked in), you **fine-tune** — adjusting model weights on your own examples.

| Concept | What it means |
|---|---|
| **Advanced fine-tuning methods** | Full fine-tuning vs. parameter-efficient methods (e.g., LoRA) — trading cost/speed vs. flexibility |
| **Synthetic data for fine-tuning** | Using a strong model to **generate** high-quality training examples when real labeled data is scarce |
| **Monitoring fine-tuned model performance** | Same observability/evaluation discipline as Domain 4, applied specifically to the fine-tuned model's outputs |
| **Lifecycle management** | Dev → validation → staged production rollout → ongoing monitoring → retirement, just like Domain 2's model lifecycle, but for a fine-tuned generative model |

### 🏗️ Real-World Artifact — Fine-Tuning Job with Synthetic Data Generation

```python
# Step 1: Generate synthetic training examples using a strong "teacher" model
synthetic_examples = []
for topic in scarce_topics:
    prompt = f"Generate 5 realistic customer support Q&A pairs about: {topic}"
    response = teacher_model.generate(prompt)
    synthetic_examples.extend(parse_qa_pairs(response))

# Step 2: Combine with real labeled data, format for fine-tuning
# training_data.jsonl
# {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# Step 3: Submit fine-tuning job
az ml job create --file finetune-job.yml
```

```yaml
# finetune-job.yml (conceptual)
type: fine_tuning
model: gpt-4o-mini
training_data: azureml:training_data_v3:1
validation_data: azureml:validation_data_v3:1
hyperparameters:
  n_epochs: 3
  learning_rate_multiplier: 0.1
tags:
  use_case: "customer-support-tone-alignment"
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Why use synthetic data | Real labeled examples are scarce/expensive — a strong model can bootstrap realistic training pairs, especially for rare/edge-case scenarios |
| Fine-tuning vs. RAG | RAG = inject facts at query time (good for frequently changing knowledge); Fine-tuning = change behavior/style/format (good for stable patterns) |
| Overfitting risk | Monitor validation loss and downstream quality metrics (Domain 4) — a fine-tuned model that memorizes training data generalizes poorly |
| Full lifecycle | Fine-tuned models still need registration, versioning, evaluation gates, and monitoring — same discipline as Domain 2, GenAI-flavored |

---

### ❓ Practice Questions — Fine-Tuning & Model Customization

**Q4.** Your company wants a support model to consistently respond in a very specific brand voice and structured JSON output format across thousands of varied queries — something prompt engineering alone hasn't reliably achieved. What is the most appropriate solution?

A) Add more retrieved documents to the RAG context
B) Fine-tune the model on labeled examples demonstrating the desired tone and output format
C) Increase the similarity threshold in retrieval
D) Switch to keyword-only search

✅ **Answer: B) Fine-tune the model on labeled examples demonstrating the desired tone and output format**

💡 **Explanation:** Consistent **style, tone, and structural formatting** across diverse inputs is a behavior-shaping problem best solved by **fine-tuning** on representative examples — RAG and retrieval tuning address *what facts* the model has access to, not *how* it consistently phrases/structures its answers.

---

**Q5.** You have very few real labeled examples of a rare customer scenario your fine-tuned model needs to handle well. What technique can help you build a sufficient training set?

A) Manually write thousands of examples by hand
B) Generate synthetic training examples using a capable model, then review/curate them
C) Skip fine-tuning for that scenario entirely
D) Duplicate the few real examples hundreds of times

✅ **Answer: B) Generate synthetic training examples using a capable model, then review/curate them**

💡 **Explanation:** The skills outline explicitly names **"create and manage synthetic data for fine-tuning."** Using a strong model to generate plausible, varied training examples (then human-reviewing for quality) is the standard technique to fill data gaps for rare scenarios — duplicating the same few real examples (D) would just cause overfitting to those exact cases, not genuine coverage.

---

**Q6.** After deploying a fine-tuned model to production, how should you ensure it continues to perform well over time?

A) Consider the job done once fine-tuning completes successfully
B) Apply the same monitoring and evaluation discipline as any production model — track quality metrics, drift, and cost, with defined retraining/refresh triggers
C) Only check performance if a customer complains
D) Re-fine-tune from scratch every day regardless of need

✅ **Answer: B) Apply the same monitoring and evaluation discipline as any production model — track quality metrics, drift, and cost, with defined retraining/refresh triggers**

💡 **Explanation:** The skills outline calls for **"monitor and optimize fine-tuned model performance"** and **"manage a fine-tuned model from development through production deployment"** — meaning the full MLOps/GenAIOps lifecycle discipline (Domains 2 and 4) applies here too. Fine-tuning isn't a "set and forget" event; it's the start of an ongoing operational responsibility.

---

## 🧠 Domain 5 Quick-Recall Cheat Sheet

- **RAG tuning levers**: similarity threshold, chunk size (+ overlap), top-k, hybrid (semantic + keyword) search, domain-specific embeddings
- **Diagnose retrieval problems**: irrelevant chunks → shrink chunk size; missed exact terms/IDs → add hybrid/keyword search
- **Validate RAG changes**: relevance metrics + A/B testing before full rollout
- **Fine-tuning**: use when prompt engineering/RAG can't achieve consistent tone/format/behavior
- **Synthetic data**: bootstrap training examples for rare scenarios using a capable model, then curate
- **Fine-tuned models still need**: full lifecycle management — evaluation, monitoring, drift/refresh triggers

---

## 🏁 You've Completed All 5 Domains — What's Next?

1. Go back through each file's **Quick-Recall Cheat Sheet** and try to explain each bullet out loud, unaided.
2. Redo every practice question **cold** (cover the answers) — track your hit rate per domain.
3. Do the hands-on labs listed in the [README](./README.md) — this exam rewards people who've actually clicked through Azure ML and Foundry, not just memorized terms.
4. Recheck the [official study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-300) close to your exam date — AI-300 is in **beta**, and weightings/topics can be refined before GA.

Good luck — you've got this. 🚀

---

⬅ [Previous: Domain 4](./04-Domain4-Quality-Assurance-Observability.md) | ⬅ [Back to README](./README.md)
