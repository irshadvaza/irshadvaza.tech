# 🧠 Microsoft AI-300: Operationalizing Machine Learning and Generative AI Solutions
### Complete Study Guide — Section-Wise & Topic-Wise (with Practice Q&A)

> **Certification:** Microsoft Certified: Machine Learning Operations (MLOps) Engineer Associate
> **Exam Code:** AI-300
> **Replaces:** DP-100 (Designing and Implementing a Data Science Solution on Azure) — retiring June 1, 2026
> **Status:** Currently in Beta (entered beta March 2026)
> **Duration:** 120 minutes | **Passing Score:** 700/1000 | **Format:** Proctored, may include interactive/lab-style items

---

## 📌 Why This Exam Exists

DP-100 tested whether you could *build* a model. AI-300 tests whether you can **run AI in production** — safely, at scale, and without breaking things at 2 AM. Think of it as the certification for the person who gets paged when a model's accuracy silently drops or a GenAI endpoint starts costing 10x more overnight.

Two disciplines, one exam:

| Discipline | What it covers |
|---|---|
| **MLOps** | Traditional ML models — training, registration, deployment, drift monitoring, retraining |
| **GenAIOps** | Generative AI apps/agents — Foundry deployments, RAG, evaluation, safety, cost/latency optimization |

Together, Microsoft calls this **AIOps**.

---

## 🗂️ Repository Structure

```
AI-300/
├── README.md                                     ← you are here
├── 01-Domain1-MLOps-Infrastructure.md            (15–20%)
├── 02-Domain2-Model-Lifecycle-Operations.md      (25–30%)
├── 03-Domain3-GenAIOps-Infrastructure.md         (20–25%)
├── 04-Domain4-Quality-Assurance-Observability.md (10–15%)
└── 05-Domain5-Optimize-GenAI-Performance.md      (10–15%)
```

Each file follows the same pattern so you can study consistently:

```
Section
  ├── 🔑 Plain-English Explanation
  ├── 🏗️ Real-World Analogy / Artifact (YAML, CLI, diagram)
  ├── 📋 Key Facts Table
  └── ❓ Practice Questions + ✅ Answers + 💡 Explanation
```

---

## 🎯 Skills Measured (Official Weighting)

| # | Domain | Weight |
|---|---|---|
| 1 | Design and implement an MLOps infrastructure | **15–20%** |
| 2 | Implement machine learning model lifecycle and operations | **25–30%** |
| 3 | Design and implement a GenAIOps infrastructure | **20–25%** |
| 4 | Implement generative AI quality assurance and observability | **10–15%** |
| 5 | Optimize generative AI systems and model performance | **10–15%** |

📊 **Study time allocation tip:** Domains 2 and 3 together are ~50% of the exam — spend half your prep time there.

---

## 👤 Who This Exam Is For

You should already be comfortable with:
- **Python** (data science background)
- **Azure Machine Learning** (workspaces, compute, pipelines, MLflow)
- **Microsoft Foundry** (formerly Azure AI Studio / Azure AI Foundry) for GenAI apps and agents
- **DevOps basics**: Git, GitHub Actions, CI/CD
- **Infrastructure as Code (IaC)**: Bicep, Azure CLI

If any of these are brand new to you, do a quick primer *before* diving into the domain files (see Study Path below).

---

## 🛣️ Suggested 6-Week Study Path

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Domain 1 – MLOps Infrastructure | Deploy a Machine Learning workspace via Bicep + GitHub Actions |
| 2 | Domain 2 (Part A) – Training & Registration | Run an MLflow-tracked training job + AutoML experiment |
| 3 | Domain 2 (Part B) – Deployment & Monitoring | Deploy a real-time endpoint, simulate data drift |
| 4 | Domain 3 – GenAIOps Infrastructure | Stand up a Foundry project, deploy a model via serverless endpoint |
| 5 | Domain 4 – Quality, Safety, Observability | Build an evaluation pipeline (groundedness, relevance) |
| 6 | Domain 5 – RAG & Fine-Tuning Optimization | Tune a RAG pipeline; run a fine-tuning job with synthetic data |

Then: 2–3 full practice-question passes across all files, focused on your weakest domain.

---

## 🧰 Hands-On Labs You Should Actually Do

1. Create an Azure ML workspace using **Bicep** (not just the portal).
2. Wire up a **GitHub Actions** workflow that provisions ML resources on push.
3. Train a model, log it with **MLflow**, register it, and deploy it as a **managed online endpoint**.
4. Deploy a foundation model in **Microsoft Foundry** via a **serverless API endpoint**.
5. Build a small **RAG pipeline** (vector index + retrieval + generation) and tune chunk size/similarity threshold.
6. Set up a **risk & safety evaluation** on a Foundry project and review the groundedness/coherence scores.

---

## 📚 Official Microsoft Resources

- [Exam AI-300 official page](https://learn.microsoft.com/en-us/credentials/certifications/exams/AI-300)
- [Official Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-300)
- [Microsoft Certified: MLOps Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/operationalizing-machine-learning-and-generative-ai-solutions/)
- [Exam Sandbox (see the UI before test day)](https://aka.ms/examdemo)

> ⚠️ **Beta-exam note:** AI-300 is in beta as of this writing. Skills-measured percentages can shift slightly before General Availability (GA) — always cross-check the official study guide link above before your exam date.

---


---

**Next →** [`01-Domain1-MLOps-Infrastructure.md`](./01-Domain1-MLOps-Infrastructure.md)
