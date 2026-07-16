# Domain 1: Design and Implement an MLOps Infrastructure (15–20%)

⬅ [Back to README](./README.md) | ➡ [Next: Domain 2 – Model Lifecycle & Operations](./02-Domain2-Model-Lifecycle-Operations.md)

---

## 🧭 Domain Overview

This domain is the "plumbing" section of the exam. Before anyone trains a model, someone has to stand up the **workspace**, wire up **compute**, secure **identity/access**, and make sure all of it is **repeatable via code** — not clicked together by hand in the portal. If Domain 2 is "run the car," Domain 1 is "build the garage, the road, and the ignition system."

Three sub-topics:
1. Create and manage resources in a Machine Learning workspace
2. Create and manage assets in a Machine Learning workspace
3. Implement Infrastructure as Code (IaC) for Machine Learning

---

## 1️⃣ Create and Manage Resources in a Machine Learning Workspace

### 🔑 Plain-English Explanation

The **Azure Machine Learning workspace** is the top-level container for everything ML-related: experiments, models, endpoints, compute, data connections. Think of it as the "project folder" that ties together storage, key vault, app insights, and container registry behind the scenes.

Key resource types you must know:

| Resource | Purpose |
|---|---|
| **Workspace** | Top-level container; auto-provisions Storage Account, Key Vault, App Insights, Container Registry |
| **Datastore** | A secure, named reference to a storage location (Blob, ADLS Gen2, etc.) — no credentials stored in code |
| **Compute Instance** | Personal, always-on dev VM for notebooks/experimentation |
| **Compute Cluster** | Auto-scaling, multi-node cluster for training jobs (scales to 0 when idle) |
| **Inference Cluster / Managed Endpoint Compute** | Compute backing real-time or batch endpoints |
| **Managed Identity + RBAC** | Controls who/what can access the workspace and its resources |

### 🏗️ Real-World Artifact — Creating a Workspace via Azure CLI

```bash
az ml workspace create \
  --name mlw-fraud-detection \
  --resource-group rg-ai300-demo \
  --location eastus \
  --storage-account stfrauddetection \
  --key-vault kv-frauddetection
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Datastore auth options | Account key, SAS token, **identity-based (recommended)** |
| Compute cluster scaling | Min nodes can be 0 (cost saving); max nodes capped by quota |
| Workspace identity types | System-assigned or user-assigned managed identity |
| Network isolation option | Private endpoint + managed VNet for the workspace |

---

### ❓ Practice Questions — Workspace Resources

**Q1.** Your team wants a compute target that automatically scales down to zero nodes when idle to minimize cost, but can scale up to handle large distributed training jobs. Which compute type should you provision?

A) Compute Instance
B) Compute Cluster
C) Kubernetes online endpoint
D) Serverless API endpoint

✅ **Answer: B) Compute Cluster**

💡 **Explanation:** A **Compute Cluster** supports autoscaling, including scaling to **0 nodes** when idle, and can scale out across multiple nodes for distributed training. A **Compute Instance** is a single, always-associated-with-one-user dev VM — it doesn't autoscale to zero the same way and is meant for interactive notebook work, not distributed training jobs. Serverless API endpoints and Kubernetes online endpoints are for **inference**, not training.

---

**Q2.** You need to let your Machine Learning workspace read training data from an Azure Data Lake Storage Gen2 account **without** storing account keys or SAS tokens anywhere in your code or pipeline YAML. What should you configure?

A) A SAS-token-based datastore
B) An identity-based datastore using the workspace's managed identity
C) Hardcode the storage account key as a pipeline parameter
D) Use anonymous public blob access

✅ **Answer: B) Identity-based datastore using the workspace's managed identity**

💡 **Explanation:** Identity-based datastores let Azure ML authenticate to storage using the **workspace's (or user's) managed identity** and Azure RBAC, eliminating the need to store secrets. This is the Microsoft-recommended, most secure pattern and is heavily emphasized in the exam's security-conscious framing of MLOps.

---

## 2️⃣ Create and Manage Assets in a Machine Learning Workspace

### 🔑 Plain-English Explanation

"Assets" are the versioned building blocks you register **inside** a workspace so they're reusable and traceable:

| Asset | What it is | Analogy |
|---|---|---|
| **Data asset** | Versioned pointer to a dataset (file, folder, or table) | A "released version" of a spreadsheet |
| **Environment** | A versioned Docker image / Conda spec defining the runtime (Python packages, CUDA, etc.) | A frozen "recipe" for the software stack |
| **Component** | A versioned, reusable unit of a pipeline (e.g., "train step," "eval step") | A LEGO brick you can snap into multiple pipelines |
| **Registry** | A workspace-independent catalog to **share** assets across multiple workspaces (e.g., dev → prod) | A company-wide app store for ML assets |

### 🏗️ Real-World Artifact — Registering an Environment (YAML)

```yaml
# environment.yml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: fraud-training-env
version: 3
conda_file: conda.yml
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
```

```bash
az ml environment create --file environment.yml --resource-group rg-ai300-demo --workspace-name mlw-fraud-detection
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Data asset types | `uri_file`, `uri_folder`, `mltable` |
| Environment sources | Curated (Microsoft-provided), custom Docker, or Conda-on-base-image |
| Component reuse | Components can be versioned and shared across pipelines *and* across workspaces via a registry |
| Registries vs. workspaces | Registry = cross-workspace sharing; Workspace = single-project scope |

---

### ❓ Practice Questions — Workspace Assets

**Q3.** Your organization has separate **dev**, **test**, and **prod** Machine Learning workspaces. You want a data scientist to train a model in the dev workspace using a curated environment, and have that *exact same* environment definition promoted and reused for retraining in the prod workspace without redefining it. What should you use?

A) Copy the Dockerfile manually into each workspace
B) A Machine Learning **registry**
C) A compute cluster shared across workspaces
D) A single shared datastore

✅ **Answer: B) A Machine Learning registry**

💡 **Explanation:** A **registry** exists independently of any single workspace and is purpose-built to **share versioned assets** — environments, models, components, data — across multiple workspaces (e.g., dev/test/prod), ensuring consistency and traceability across the promotion pipeline. Compute and datastores are workspace-scoped resources, not asset-sharing mechanisms.

---

**Q4.** You are designing a training pipeline made of a "data prep" step and a "train" step. You want each step to be independently versioned, tested, and reused in other pipelines (e.g., a batch scoring pipeline). What asset type should each step be authored as?

A) Environment
B) Component
C) Data asset
D) Compute target

✅ **Answer: B) Component**

💡 **Explanation:** A **component** is a self-contained, versioned unit of code (with its own inputs/outputs/environment) designed to be composed into one or more pipelines — exactly the reusability described. Environments define the runtime, not the logic; data assets are just data.

---

## 3️⃣ Implement Infrastructure as Code (IaC) for Machine Learning

### 🔑 Plain-English Explanation

Domain 1's heaviest exam-weight sub-topic. The whole point of MLOps is **repeatability** — nothing should be a one-off portal click. This topic tests whether you can:
- Provision ML resources with **Bicep** and **Azure CLI**
- Automate that provisioning with **GitHub Actions**
- Secure the pipeline (GitHub → Azure) using **federated identity / OIDC**, not stored secrets
- Restrict **network access** (private endpoints, managed VNet)
- Manage **source control** for ML projects with Git

### 🏗️ Real-World Artifact — GitHub Actions Workflow Using OIDC + Bicep

```yaml
# .github/workflows/deploy-ml-infra.yml
name: Deploy ML Infrastructure

on:
  push:
    branches: [main]
    paths: ['infra/**']

permissions:
  id-token: write   # required for OIDC federated login
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC — no client secret stored)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy Bicep template
        run: |
          az deployment group create \
            --resource-group rg-ai300-demo \
            --template-file infra/main.bicep \
            --parameters infra/main.parameters.json
```

```bicep
// infra/main.bicep (excerpt)
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: 'mlw-fraud-detection'
  location: resourceGroup().location
  identity: { type: 'SystemAssigned' }
  properties: {
    friendlyName: 'Fraud Detection Workspace'
    publicNetworkAccess: 'Disabled'   // private networking enforced
  }
}
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Recommended GitHub↔Azure auth | **OpenID Connect (OIDC) / federated credentials** — no long-lived client secrets |
| IaC tools in scope | **Bicep** and **Azure CLI** (ARM/Terraform not the focus of this exam) |
| Network restriction options | Private endpoints, disable public network access, managed VNet for workspace |
| Source control | Git branching strategy for ML code, notebooks stripped of output before commit, `.gitignore` for large artifacts |

---

### ❓ Practice Questions — IaC for Machine Learning

**Q5.** You need to configure a GitHub Actions workflow to authenticate to Azure and deploy Machine Learning infrastructure **without** storing a client secret in GitHub repository secrets. Which authentication approach should you configure?

A) A Personal Access Token (PAT)
B) Service principal with a stored client secret
C) OpenID Connect (OIDC) federated credentials
D) A shared storage account key

✅ **Answer: C) OpenID Connect (OIDC) federated credentials**

💡 **Explanation:** OIDC federated identity lets GitHub Actions request short-lived tokens directly from Microsoft Entra ID **without any stored secret** — the trust relationship is established once (federated credential on an app registration / managed identity), and each workflow run proves its identity dynamically. This is the current Microsoft-recommended best practice and squarely testable under "automate resource provisioning using GitHub Actions."

---

**Q6.** A security team requires that your Machine Learning workspace be completely unreachable from the public internet, with all traffic to the workspace, its storage, and Key Vault routed privately within the VNet. Which two configurations should you implement? (Choose 2)

A) Enable a Compute Instance with a public IP
B) Disable public network access on the workspace
C) Configure private endpoints for the workspace and its dependent resources
D) Use a SAS token with a long expiration

✅ **Answer: B) Disable public network access on the workspace, and C) Configure private endpoints for the workspace and its dependent resources**

💡 **Explanation:** Locking down a workspace network-wise requires **both**: (1) turning off public network access at the workspace level, and (2) provisioning **private endpoints** so traffic to the workspace, storage account, key vault, and container registry all flows over the private VNet instead of the public internet. A or D would actually weaken security.

---

**Q7.** Your team wants every change to `infra/*.bicep` files to automatically re-provision the affected Azure ML resources, but only after a pull request has been approved and merged to `main`. What GitHub Actions trigger configuration best supports this?

A) `on: schedule` with a nightly cron job
B) `on: push` scoped to the `main` branch and the `infra/**` path
C) `on: workflow_dispatch` only, run manually every time
D) A pre-commit Git hook on developer laptops

✅ **Answer: B) `on: push` scoped to the `main` branch and the `infra/**` path**

💡 **Explanation:** Combining a **branch filter** (`main`, meaning it only fires after merge — which implies PR approval as part of your branch protection rules) with a **path filter** (`infra/**`) ensures the deployment workflow runs automatically and *only* when relevant infrastructure code changes land on the protected branch. Manual dispatch and local hooks don't provide the automation and governance the scenario requires.

---

## 🧠 Domain 1 Quick-Recall Cheat Sheet

- **Workspace** = the top-level container (auto-creates Storage, Key Vault, App Insights, ACR)
- **Datastore** = secure pointer to storage; prefer **identity-based** auth
- **Compute Cluster** (autoscale, can hit 0 nodes) vs. **Compute Instance** (personal dev VM, always-on)
- **Assets**: Data asset, Environment, Component — all versioned; **Registry** = share across workspaces
- **IaC**: Bicep + Azure CLI + GitHub Actions; use **OIDC**, not secrets
- **Network security**: private endpoints + disable public access + managed VNet

---

⬅ [Back to README](./README.md) | ➡ [Next: Domain 2 – Model Lifecycle & Operations](./02-Domain2-Model-Lifecycle-Operations.md)
