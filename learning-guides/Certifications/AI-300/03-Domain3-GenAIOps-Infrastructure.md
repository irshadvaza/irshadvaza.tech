# Domain 3: Design and Implement a GenAIOps Infrastructure (20–25%)

⬅ [Previous: Domain 2](./02-Domain2-Model-Lifecycle-Operations.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 4 – Quality Assurance & Observability](./04-Domain4-Quality-Assurance-Observability.md)

---

## 🧭 Domain Overview

If Domain 1–2 is "operate a traditional ML model," Domain 3 is the same discipline applied to **generative AI** — foundation models, agents, and prompts — built on **Microsoft Foundry** (the evolved Azure AI Studio / Azure AI Foundry platform). Second-largest domain on the exam (20–25%).

Three sub-topics:
1. Implement Foundry environments and platform configuration
2. Deploy and manage foundation models for production workloads
3. Implement prompt versioning and management with source control

---

## 1️⃣ Implement Foundry Environments and Platform Configuration

### 🔑 Plain-English Explanation

Before deploying any GenAI model, you need a **Foundry resource + project** — the GenAI equivalent of the ML workspace — properly secured.

| Concept | What it means |
|---|---|
| **Foundry resource** | Top-level Azure resource hosting one or more projects |
| **Foundry project** | Scoped workspace for a specific GenAI solution (models, agents, evaluations) |
| **Managed identity + RBAC** | Same principle as Domain 1 — no hardcoded keys, least-privilege roles (e.g., *Azure AI Developer*, *Cognitive Services User*) |
| **Private networking** | Private endpoints so the Foundry project isn't reachable from the public internet |
| **IaC via Bicep/CLI** | Same discipline as Domain 1, applied to Foundry resources |

### 🏗️ Real-World Artifact — Provisioning a Foundry Project (Bicep excerpt)

```bicep
resource foundryResource 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'foundry-contoso-genai'
  location: 'eastus'
  kind: 'AIServices'
  identity: { type: 'SystemAssigned' }
  properties: {
    publicNetworkAccess: 'Disabled'
    disableLocalAuth: true      // forces Entra ID / managed identity auth, no API keys
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-11-01' = {
  name: 'pe-foundry-contoso'
  location: 'eastus'
  properties: {
    subnet: { id: vnetSubnetId }
    privateLinkServiceConnections: [{
      name: 'foundry-connection'
      properties: {
        privateLinkServiceId: foundryResource.id
        groupIds: ['account']
      }
    }]
  }
}
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| `disableLocalAuth: true` | Forces Entra ID token auth instead of API keys — best practice |
| RBAC roles to know | *Azure AI Developer*, *Cognitive Services OpenAI User*, *Cognitive Services Contributor* |
| Network isolation | Private endpoint + disabled public network access, same pattern as Domain 1 |
| Project vs. resource | One Foundry **resource** can host multiple **projects** (e.g., per team or per app) |

---

### ❓ Practice Questions — Foundry Environments

**Q1.** Your security team mandates that no API keys be used to authenticate to your Foundry resource — all calls must use Microsoft Entra ID identities. Which configuration should you set on the Foundry resource?

A) `publicNetworkAccess: Enabled`
B) `disableLocalAuth: true`
C) Rotate the API key weekly instead
D) Store the API key in a GitHub Actions secret

✅ **Answer: B) `disableLocalAuth: true`**

💡 **Explanation:** Setting **`disableLocalAuth: true`** disables key-based ("local") authentication entirely, forcing all callers to authenticate via **Microsoft Entra ID** (using managed identities or service principals) — directly satisfying the "no API keys" requirement. Rotating keys still leaves key-based auth as a valid path.

---

**Q2.** You want to isolate your Foundry project so that it's completely unreachable from the public internet, with all traffic flowing through your organization's VNet. What two things should you configure? (Choose 2)

A) Disable public network access on the Foundry resource
B) Configure a private endpoint connecting the Foundry resource to your VNet
C) Enable anonymous access for faster development
D) Use a longer API key expiration

✅ **Answer: A) Disable public network access on the Foundry resource, and B) Configure a private endpoint connecting the Foundry resource to your VNet**

💡 **Explanation:** Exactly mirrors the Domain 1 network-isolation pattern: **disable public access** + **stand up a private endpoint**. This is a recurring exam pattern across both MLOps and GenAIOps domains — expect it tested in both contexts.

---

## 2️⃣ Deploy and Manage Foundation Models for Production Workloads

### 🔑 Plain-English Explanation

This is the heart of GenAIOps: getting a foundation model (like GPT-family, Llama, Phi, etc.) live and choosing the right **deployment/compute model** for your traffic pattern.

| Deployment Option | Best For |
|---|---|
| **Serverless API endpoint (pay-as-you-go)** | Variable/unpredictable traffic, fast to stand up, no capacity management |
| **Managed compute (dedicated)** | Predictable/high-volume traffic, more control over the hosting VM |
| **Provisioned Throughput Units (PTUs)** | High-volume, latency-sensitive, consistent workloads needing **guaranteed** throughput (reserved capacity, not shared) |

| Concept | What it means |
|---|---|
| **Model selection** | Match model size/capability/cost to the use case (don't use a giant model for simple classification) |
| **Model versioning** | Foundation models get version updates; pin versions for production stability |
| **Production deployment strategy** | Similar canary/blue-green ideas as Domain 2, applied to model swaps |

### 🏗️ Real-World Artifact — Deploying via Serverless vs. PTU

```bash
# Serverless (pay-as-you-go) deployment — good for bursty/dev traffic
az cognitiveservices account deployment create \
  --name foundry-contoso-genai \
  --resource-group rg-ai300-demo \
  --deployment-name gpt-4o-serverless \
  --model-name gpt-4o \
  --model-version "2024-11-20" \
  --sku-name "Standard" \
  --sku-capacity 1

# Provisioned Throughput deployment — for guaranteed, high-volume production traffic
az cognitiveservices account deployment create \
  --name foundry-contoso-genai \
  --resource-group rg-ai300-demo \
  --deployment-name gpt-4o-ptu-prod \
  --model-name gpt-4o \
  --model-version "2024-11-20" \
  --sku-name "ProvisionedManaged" \
  --sku-capacity 100
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Serverless billing | Pay-per-token, scales automatically, best for unpredictable load |
| PTU billing | Reserved/hourly capacity, predictable cost, **guaranteed** latency/throughput at scale |
| When to pick PTU | High, steady request volume where shared/serverless capacity risks throttling |
| Model version pinning | Prevents an unplanned auto-update from silently changing production behavior |

---

### ❓ Practice Questions — Foundation Model Deployment

**Q3.** Your customer-support chatbot handles a consistently high volume of requests (millions/day) and cannot tolerate latency spikes caused by shared-capacity throttling. Which deployment option best fits this requirement?

A) Serverless (pay-as-you-go) API endpoint
B) Provisioned Throughput Units (PTU)
C) A free-tier trial deployment
D) A Compute Instance running the model locally

✅ **Answer: B) Provisioned Throughput Units (PTU)**

💡 **Explanation:** **PTUs** reserve dedicated capacity for your deployment, giving **predictable latency and guaranteed throughput** — ideal for high, steady-volume production workloads where shared serverless capacity could throttle under load. Serverless is better suited to variable/lower-volume or dev/test traffic.

---

**Q4.** A startup is prototyping a new GenAI feature with unpredictable, low-to-moderate traffic and wants to avoid managing or paying for reserved capacity. Which deployment type should they choose?

A) Provisioned Throughput Units (PTU)
B) Serverless API endpoint
C) A dedicated Kubernetes cluster
D) An on-premises GPU server

✅ **Answer: B) Serverless API endpoint**

💡 **Explanation:** Serverless (pay-as-you-go) endpoints require **no capacity planning**, bill per token consumed, and scale automatically — the right fit for unpredictable or early-stage traffic where committing to reserved PTU capacity would be wasteful.

---

**Q5.** Your production application is pinned to `gpt-4o` version `2024-11-20`. Microsoft releases a new default version. What should you do to avoid unplanned behavior changes in production?

A) Do nothing — deployments always auto-update safely
B) Explicitly test the new model version in a non-production deployment first, then intentionally update the version pin once validated
C) Immediately delete the old deployment
D) Switch to a different vendor entirely

✅ **Answer: B) Explicitly test the new model version in a non-production deployment first, then intentionally update the version pin once validated**

💡 **Explanation:** Foundation models evolve; the exam's "implement model versioning and production deployment strategies" objective expects you to treat model version changes like any other production change — **validate in a lower environment, then deliberately roll forward** — rather than letting an implicit auto-update reach production untested.

---

## 3️⃣ Implement Prompt Versioning and Management with Source Control

### 🔑 Plain-English Explanation

Prompts are **code** in GenAIOps — they should be designed deliberately, tested against variants, and version-controlled just like application source code, not edited ad hoc in a chat window.

| Concept | What it means |
|---|---|
| **Prompt design/development** | Structured prompt engineering — system messages, few-shot examples, grounding instructions |
| **Prompt variants** | Multiple candidate versions of a prompt, A/B compared on quality metrics |
| **Version control for prompts** | Store prompt templates as files in **Git**, tracked with commit history, PRs, and rollback |

### 🏗️ Real-World Artifact — Prompt File Under Git Version Control

```
prompts/
├── customer_support/
│   ├── v1_baseline.prompty
│   ├── v2_added_tone_guidance.prompty
│   └── v3_added_refusal_examples.prompty
```

```yaml
# v3_added_refusal_examples.prompty (Prompty format)
---
name: CustomerSupportAgent
model:
  api: chat
  configuration:
    type: azure_openai
    azure_deployment: gpt-4o-ptu-prod
---
system:
You are a helpful, concise customer support agent for Contoso.
Always ground answers in the provided knowledge base context.
If the answer isn't in the context, say you don't know — never guess.

user:
{{question}}
```

```bash
git add prompts/customer_support/v3_added_refusal_examples.prompty
git commit -m "Add refusal examples to reduce hallucination on out-of-scope questions"
git tag prompt-v3-customer-support
```

### 📋 Key Facts Table

| Fact | Detail |
|---|---|
| Prompt file format | `.prompty` files are a common Microsoft-supported way to version prompts with model config attached |
| Comparing variants | Run each variant against the same evaluation dataset, compare quality metrics (see Domain 4) |
| Why Git for prompts | Full history, diffing, PR review, rollback — same governance as application code |
| Anti-pattern | Editing the "live" system prompt directly in a portal UI with no history |

---

### ❓ Practice Questions — Prompt Versioning

**Q6.** Your team wants to compare two candidate system prompts for a support chatbot to determine which produces more accurate, grounded answers before choosing one for production. What should you do?

A) Deploy both to production simultaneously and let users pick
B) Create prompt variants and evaluate both against the same test dataset using quality metrics
C) Ask a single team member to eyeball a few responses and decide
D) Only test the prompt that "feels" better

✅ **Answer: B) Create prompt variants and evaluate both against the same test dataset using quality metrics**

💡 **Explanation:** The skills outline specifically calls out **"create prompt variants and compare performance across different prompts."** A rigorous, repeatable comparison requires running each variant against a **consistent evaluation dataset** and scoring both with quality metrics (groundedness, relevance — see Domain 4), not subjective judgment or uncontrolled production A/B exposure.

---

**Q7.** Why should prompt templates be stored in a Git repository rather than edited directly in a chat playground or portal UI?

A) Git is required for the model to function
B) It provides version history, code review via pull requests, and the ability to roll back to a previous prompt if a new version underperforms
C) It makes the prompts load faster at runtime
D) Portal UIs cannot store text

✅ **Answer: B) It provides version history, code review via pull requests, and the ability to roll back to a previous prompt if a new version underperforms**

💡 **Explanation:** Treating prompts as versioned artifacts in **source control** gives you the same governance benefits as application code: auditability, peer review before changes reach production, and a fast, reliable rollback path if a new prompt version regresses quality — core to the "GenAIOps" discipline this exam validates.

---

## 🧠 Domain 3 Quick-Recall Cheat Sheet

- **Foundry setup**: resource → project; `disableLocalAuth: true` + private endpoints for security
- **Model deployment**: Serverless = variable traffic, pay-per-token; **PTU** = guaranteed throughput for high, steady volume
- **Model versioning**: Pin versions; test new versions before rolling forward in production
- **Prompts = code**: version in Git, compare variants against eval datasets, never edit "live" ad hoc

---

⬅ [Previous: Domain 2](./02-Domain2-Model-Lifecycle-Operations.md) | ⬅ [Back to README](./README.md) | ➡ [Next: Domain 4 – Quality Assurance & Observability](./04-Domain4-Quality-Assurance-Observability.md)
