# 📘 Chapter 1: Azure ML Fundamentals
### Learning Guide — Section-Wise & Topic-Wise (with Screenshots)

> **Source:** `Intro to Azure ML.pptx`
> **Level:** Beginner → Foundational
> **Best paired with:** [AI-300 Exam Guide](../../Certifications/AI-300/README.md) → Domain 1 (MLOps Infrastructure)

---

## 🧭 Chapter Overview

This chapter introduces **Azure Machine Learning (Azure ML) ** — the umbrella Azure service for building, training, deploying, and monitoring **both** classical ML models and generative AI applications. Every later chapter (compute, pipelines, deployment, monitoring) builds directly on the concepts introduced here, so treat this as the foundation, not a skimmable intro.

### 📑 Sections in This Chapter

| # | Section | What You'll Learn |
|---|---|---|
| 1 | [What Is Azure Machine Learning?](#section-1--what-is-azure-machine-learning) | The big picture — why it exists |
| 2 | [Azure ML = GenAI + Classical ML](#section-2--azure-ml--genai--classical-ml) | The two AI paradigms it unifies |
| 3 | [The Azure ML Ecosystem](#section-3--the-azure-ml-ecosystem) | What gets provisioned behind the scenes |
| 4 | [The Azure Machine Learning Studio](#section-4--the-azure-machine-learning-studio) | Where you'll actually work day-to-day |
| 5 | [Azure ML Workspace Features](#section-5--azure-ml-workspace-features) | The full feature map of the workspace |
| 6 | [Azure Machine Learning Designer](#section-6--azure-machine-learning-designer) | Low-code pipeline building |
| 7 | [GenAI with ML Workspaces](#section-7--genai-with-ml-workspaces) | Model catalog + Prompt flow |

---

## Section 1 — What Is Azure Machine Learning?

### 🔑 Plain-English Explanation

**Azure Machine Learning** is Microsoft's cloud platform for the **entire ML/AI lifecycle** — not just training a model, but everything around it: provisioning compute, tracking experiments, versioning data and models, deploying to production, and monitoring once it's live.

Think of it this way: if you've ever trained a model in a personal Jupyter notebook on your laptop, Azure ML is what happens when that notebook needs to become a **team sport** — reproducible, auditable, scalable, and safe to run in production.

> 💡 **Real-world analogy:** A local Jupyter notebook is like cooking dinner for yourself. Azure ML is running a restaurant kitchen — same basic skill (cooking/modeling), but now you need consistent recipes (reproducible training), inventory tracking (data/model versioning), health inspections (governance/Responsible AI), and the ability to serve hundreds of customers at once (scalable deployment).

### 📋 Why It Exists — Key Facts

| Problem Without Azure ML | How Azure ML Solves It |
|---|---|
| "It worked on my laptop" | Standardized, versioned **environments** (Section 5) |
| No record of what produced a model | **MLflow experiment tracking** built in |
| Manually SSH-ing into a GPU box | Managed **compute clusters/instances** (auto-provision, auto-scale) |
| Models stuck in notebooks | One-click **deployment to endpoints** |
| No idea if a model degraded in production | Built-in **monitoring & drift detection** |

---

## Section 2 — Azure ML = GenAI + Classical ML

![Azure ML supports both Generative AI and Classical ML paradigms](../images/03-auto-provisioned-resources.png)
*(See Section 3 for the actual portal screenshot of provisioned resources — this section is conceptual.)*

### 🔑 Plain-English Explanation

The single most important mental model for this chapter: **Azure ML is not just "the classical ML tool."** As of the current platform (increasingly branded as part of **Microsoft Foundry**), it's a **unified workspace** for two AI paradigms:

| Paradigm | What It's For | Example Techniques |
|---|---|---|
| **Classical ML** | Predictive modeling on structured/tabular or labeled data | Classification, regression, forecasting, clustering |
| **Generative AI** | Creating new content, reasoning, and language-driven applications | Large language models (LLMs), embeddings, multimodal models |

Both paradigms live inside the **same workspace**, share the **same compute**, and go through the **same operational discipline** (tracking, versioning, deployment, monitoring) — which is exactly why a certification like AI-300 groups "MLOps" and "GenAIOps" together as **AIOps**.

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Classical ML use cases | Fraud detection (classification), sales forecasting (regression), customer segmentation (clustering) |
| GenAI use cases | Chatbots (LLMs), semantic search (embeddings), document Q&A (RAG), image+text apps (multimodal) |
| Shared workspace benefit | One place to build, train, evaluate, **and deploy** both types of models — no separate toolchains |
| Platform naming note | You'll see the UI now co-branded **"Microsoft Foundry \| Azure Machine Learning"** — Microsoft is unifying the ML and GenAI tooling under one front door |

### ❓ Quick Check

**Q1.** Your team needs to build both a churn-prediction model (using structured customer data) and a customer-support chatbot (using an LLM). Can both be built and managed in the same Azure ML workspace?

✅ **Answer: Yes.** Azure ML's workspace is explicitly designed as a **unified environment** for both classical ML (churn prediction = classification) and generative AI (chatbot = LLM-based) — they can share the same workspace, compute resources, and governance controls, though they'll typically use different specific tools within it (e.g., AutoML/Designer for churn, Model Catalog/Prompt flow for the chatbot).

---

## Section 3 — The Azure ML Ecosystem

### 🔑 Plain-English Explanation

When you create a single Azure ML **workspace**, Azure doesn't just create one resource — it automatically provisions a small **ecosystem** of supporting Azure services behind the scenes. Understanding this is critical for both cost management and troubleshooting (e.g., "why do I suddenly have a Key Vault I didn't explicitly create?").

### 🖼️ Screenshot — What Gets Auto-Provisioned

![Azure Resource Group showing the workspace and its auto-provisioned dependencies](images/03-auto-provisioned-resources.png)

*This is a real Azure Resource Group view after creating one workspace named `AI-300-ML-Workspace`. Notice how **one workspace creation** resulted in **six additional resources**.*

### 📋 Key Facts Table

| Auto-Provisioned Resource | Purpose |
|---|---|
| **Storage Account** | Stores datasets, model artifacts, notebooks, logs |
| **Key Vault** | Securely stores secrets, connection strings, and credentials |
| **Log Analytics Workspace** | Central log aggregation for the workspace's diagnostic data |
| **Application Insights** | Application-level telemetry — request rates, failures, performance |
| **Action Group / Smart Detector Alert Rule** | Auto-configured alerting (e.g., "Failure Anomalies") built on Application Insights |

> ⚠️ **Cost tip:** Because these resources are auto-created, deleting *just* the workspace from the portal without cleaning up its dependents can leave orphaned (and billed) resources behind. Always review the full resource group before decommissioning.

### ❓ Quick Check

**Q2.** You deleted an Azure ML workspace last month but your bill still shows charges this month. What is the most likely explanation?

✅ **Answer:** The workspace's **auto-provisioned dependent resources** (Storage Account, Key Vault, Log Analytics Workspace, Application Insights) are **separate Azure resources** that are not automatically deleted just because the parent workspace was removed — they must be cleaned up explicitly (or by deleting the entire resource group) to fully stop billing.

---

## Section 4 — The Azure Machine Learning Studio

### 🔑 Plain-English Explanation

The **Azure Machine Learning Studio** is the web-based UI where you'll spend the vast majority of your working time. If the **workspace** is the container/backend, the **Studio** is the front-end control panel for it — notebooks, pipelines, jobs, models, endpoints, and the Model Catalog all live here.

You get to the Studio from the Azure Portal by opening your workspace resource and clicking **"Launch studio."**

### 🖼️ Screenshot — Getting to the Studio from the Azure Portal

![Azure Portal workspace overview page with Access control and Launch studio highlighted](images/04-portal-workspace-overview.png)

*The Azure Portal view of a workspace resource (`mlw-dp100-labs`). Note two things highlighted here: **Access control (IAM)** (left) — where you manage who can do what in this workspace — and the **"Launch studio"** button (bottom) — your doorway into the actual working environment.*

### 🖼️ Screenshot — Inside the Studio (Home Page)

![Azure ML Studio home page showing Generative AI with Prompt flow templates and model shortcuts](images/05-studio-home-page.png)

*Once inside, the Studio home page surfaces quick-start templates (like "Multi-Round Q&A on Your Data"), trending Generative AI models, and the full left-hand navigation menu — Notebooks, Automated ML, Designer, Prompt flow, Data, Jobs, Components, Pipelines, Environments, Models, and more.*

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Portal vs. Studio | **Azure Portal** = manage the resource itself (access control, networking, deletion) |
| | **Azure ML Studio** = do the actual data science / GenAI work |
| Access control location | **Access control (IAM)** in the Portal — controls role-based access (RBAC) to the workspace |
| Studio left-nav sections | **Authoring** (Notebooks, AutoML, Designer, Prompt flow), **Assets** (Data, Jobs, Components, Pipelines, Environments, Models) |
| Studio web URL | Available directly on the Portal's workspace Overview page (`Studio web URL` field) |

### ❓ Quick Check

**Q3.** A new team member asks you: "Do I manage who has access to our ML workspace inside the Studio, or somewhere else?" What's the correct answer?

✅ **Answer:** Access control (RBAC / **IAM**) is managed at the **Azure Portal** level, on the workspace resource itself — not inside the Studio. The Studio is where you do the day-to-day ML/GenAI work (notebooks, pipelines, models); the Portal is where you manage the resource's identity, networking, and access permissions.

---

## Section 5 — Azure ML Workspace Features

### 🔑 Plain-English Explanation

This is the **feature map** of everything a workspace enables — worth memorizing as a checklist, since each bullet maps to a real capability (and, notably, closely mirrors the AI-300 exam's Domain 1 & 2 objectives).

### 📋 Full Feature Breakdown

| Category | Capability |
|---|---|
| **Compute** | Deploy Compute Instances, Compute Clusters, Kubernetes (K8s) clusters, and Serverless Compute |
| **Experimentation** | Train and track models with **MLflow** and logged metrics |
| **Pipelines** | Work with reusable **components** and multi-step **pipelines** |
| **Frameworks** | Build your model using open-source ML frameworks (scikit-learn, PyTorch, TensorFlow, etc.) |
| **Collaboration** | Work together using **Python Notebooks** inside the Studio |
| **Model Governance** | Register models as **artifacts**; create and share via **Registries** |
| **Data Management** | Register **Datastores** and **Data assets**; bring in data from Azure Blob Storage, ADLS Gen2, etc. |
| **Deployment & Ops** | Deploy models to **endpoints**, then monitor and evaluate them in production |

> 💡 **Why this table matters for AI-300:** Nearly every row above maps directly to a graded skill in Domain 1 ("Create and manage resources/assets") and Domain 2 ("Orchestrate model training," "Deploy models," "Monitor and maintain models") of the AI-300 exam. This slide is essentially a compressed exam syllabus for MLOps.

### 🏗️ Real-World Artifact — Where Each Feature Lives in the Studio Nav

```
Azure ML Studio
├── Authoring
│   ├── Notebooks         → Python Notebooks (Collaboration)
│   ├── Automated ML      → AutoML experimentation
│   ├── Designer          → Low-code pipelines (see Section 6)
│   └── Prompt flow       → GenAI orchestration (see Section 7)
├── Assets
│   ├── Data              → Datastores + Data assets
│   ├── Jobs               → Training runs, tracked via MLflow
│   ├── Components         → Reusable pipeline building blocks
│   ├── Pipelines          → Multi-step training/scoring workflows
│   ├── Environments        → Versioned runtime specs (Conda/Docker)
│   └── Models              → Registered model artifacts
└── Manage
    └── Compute             → Instances, Clusters, K8s, Serverless
```

### ❓ Quick Check

**Q4.** You want to run the exact same experiment logic on your laptop's small dataset today, and on a full production dataset across multiple GPU nodes next month, without rewriting your training code. Which two workspace features make this possible? (Choose 2)

A) Notebooks
B) Compute (Instances *and* Clusters)
C) Registries
D) Environments

✅ **Answer: B) Compute, and D) Environments**

💡 **Explanation:** A versioned **Environment** guarantees the exact same runtime/dependencies regardless of scale, while swapping from a **Compute Instance** (single dev VM, small dataset) to a **Compute Cluster** (multi-node, autoscaling) lets the same code run at production scale — this combination is precisely what makes Azure ML training code portable from laptop-scale to production-scale.

---

## Section 6 — Azure Machine Learning Designer

### 🔑 Plain-English Explanation

The **Designer** is Azure ML's **low-code, drag-and-drop pipeline builder**. Instead of writing Python to wire together data prep → training → scoring, you connect visual blocks on a canvas. It's aimed squarely at:

- **Low-code developers** who aren't primarily Python engineers
- **Rapid prototyping** — get an end-to-end pipeline running in minutes
- **Iteration** — swap one block (e.g., a different algorithm) without touching the rest of the graph

### 🖼️ Screenshot — A Completed Designer Pipeline

![Azure ML Designer showing a completed image classification pipeline with Prep Data, Train, and Score nodes](images/06-designer-pipeline.png)

*A real Designer pipeline (`image_classification_keras_minist_convnet`) with three connected nodes — **Prep Data → Train Image Classification Keras → Score Image Classification Keras** — each showing a green "Completed" status. The right-hand panel shows the **Outputs + logs** tab, including the actual test accuracy (`0.899...`) logged from the run.*

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Best for | Low-code developers, quick prototyping, teaching/demoing ML concepts visually |
| Each node represents | A **component** (the same reusable asset type mentioned in Section 5) |
| Pipeline output | Same as code-based pipelines — logged metrics, registered models, downstream deployment |
| Relationship to code-first pipelines | Designer pipelines and SDK/CLI-authored pipelines both ultimately run as **jobs** and can be inspected the same way in the Studio |

### ❓ Quick Check

**Q5.** A junior analyst with strong domain knowledge but limited Python experience needs to quickly prototype an image classification pipeline. Which Azure ML authoring tool best fits their skill level and goal?

✅ **Answer: Azure Machine Learning Designer.** It's explicitly built for **low-code developers** doing **rapid prototyping and iteration** — letting the analyst assemble a working pipeline (prep → train → score) visually, without needing to author the orchestration code by hand.

---

## Section 7 — GenAI with ML Workspaces

### 🔑 Plain-English Explanation

This section is where classical ML tooling gives way to **generative AI-specific** tooling, all still inside the same workspace:

| Tool | What It Does |
|---|---|
| **Model Catalog** | Browse and deploy from **thousands of models** — Microsoft, OpenAI, Meta (Llama), Mistral, and other open-source/partner models |
| **Prompt flow** | A **low-code GenAI microservice builder** — chain prompts, retrieval steps, and logic into an executable, testable flow |

### 🖼️ Screenshot — Model Catalog & Prompt Flow in the Studio Nav

![Azure ML Studio with Model catalog and Prompt flow highlighted in the left navigation](images/07-model-catalog-promptflow.png)

*Both **Model catalog** (under the main nav) and **Prompt flow** (under Authoring) are highlighted. Below them, the Studio home page surfaces ready-to-run GenAI templates like "Multi-Round Q&A on Your Data" and trending models such as `grok-4-1-fast-reasoning`, `MedImageParse3D`, and `Phi-4-Reasoning-Vision-15B`.*

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Model Catalog scale | "1000's of models" spanning proprietary and open-source, multiple modalities (chat, vision, image segmentation) |
| Prompt flow purpose | Orchestrate multi-step GenAI logic (retrieve → prompt → post-process) as a visual, low-code flow |
| Notebook samples provided | Studio ships ready-made notebooks like "Index and search your own data with GPT" and "Distributed GPU training" |
| Relationship to Section 2 | This is the concrete, hands-on realization of the "GenAI" half of "Azure ML = GenAI + Classical ML" |

### ❓ Quick Check

**Q6.** Your team wants to quickly build and test a "Q&A on your own documents" chatbot without writing a full custom orchestration application from scratch. Which two Studio capabilities would you use together? (Choose 2)

A) Azure ML Designer
B) Model Catalog (to select/deploy an LLM)
C) Prompt flow (to orchestrate retrieval + prompting logic)
D) Compute Clusters (for distributed classical ML training)

✅ **Answer: B) Model Catalog, and C) Prompt flow**

💡 **Explanation:** You'd deploy a suitable LLM from the **Model Catalog**, then use **Prompt flow** to wire together the retrieval-augmented generation (RAG) logic — retrieving relevant document chunks and feeding them into the prompt. The Designer (A) is oriented at classical ML pipelines, and Compute Clusters (D) are a supporting resource, not the GenAI orchestration layer itself.

---

## 🧠 Chapter 1 Quick-Recall Cheat Sheet

- Azure ML = **unified workspace** for **Classical ML** (prediction) **and** GenAI (LLMs, embeddings, multimodal)
- Creating a workspace **auto-provisions**: Storage Account, Key Vault, Log Analytics, Application Insights
- **Azure Portal** = manage the resource (access control, networking) | **Azure ML Studio** = do the actual work
- Workspace features span: Compute, MLflow tracking, Pipelines/Components, Notebooks, Model Registry, Datastores, Endpoints
- **Designer** = low-code, drag-and-drop pipelines — great for rapid prototyping
- **Model Catalog** = browse/deploy 1000s of foundation models | **Prompt flow** = low-code GenAI orchestration

---

## ✅ Chapter 1 Summary Table (Print This)

| Concept | One-Line Definition |
|---|---|
| Workspace | Top-level container tying together all ML/GenAI resources |
| Studio | Web UI for day-to-day authoring, training, and deployment work |
| Compute Instance | Personal, always-on dev VM |
| Compute Cluster | Autoscaling multi-node compute for training/batch jobs |
| MLflow | Experiment tracking (params, metrics, model artifacts) |
| Component | Reusable, versioned pipeline building block |
| Pipeline | Multi-step, chained workflow (e.g., prep → train → score) |
| Designer | Low-code, visual pipeline builder |
| Model Catalog | Repository of deployable foundation models |
| Prompt flow | Low-code GenAI application/microservice builder |
| Registry | Cross-workspace sharing of models/environments/components |

---

📌 **Next chapter (paste your next PPT):** Likely candidates based on this deck's trajectory — *Compute & Environments Deep Dive*, *Data Assets & Datastores*, or *Training with AutoML & Notebooks*. Send the next `.pptx` and I'll build Chapter 2 in the same format.
