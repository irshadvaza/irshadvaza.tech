[Home](../../index.md) | [Learning Guides](../README.md) | [Copilot Studio](README.md) | [Next Lesson →](02-first-agent.md)

---

# 📘 Lesson 1 — Introduction to Microsoft Copilot Studio

> **Understand what Copilot Studio is, where it fits, and set up your environment — before writing a single line of anything.**

**⏱ Time:** 45 minutes &nbsp;|&nbsp; **Level:** 🟢 Beginner &nbsp;|&nbsp; **Prerequisites:** None

---

## 📋 What You'll Learn

- [ ] What an AI agent is and why it matters
- [ ] How Copilot Studio fits inside the Microsoft AI ecosystem
- [ ] When to use Copilot Studio vs other tools
- [ ] How to set up your free trial environment
- [ ] A full tour of the Copilot Studio interface
- [ ] The 5 core concepts you must understand before building

---

## 1.1 🤔 What Problem Does Copilot Studio Solve?

Think about how your organization handles repetitive questions today:

```
❌ Employee emails HR: "How many leave days do I have left?"
   → HR checks system → replies 24 hours later

❌ Customer calls support: "What's the status of my order?"
   → Agent puts them on hold → checks 3 systems → answers

❌ IT gets 200 password reset requests per week
   → Each one takes 10 minutes of human time
```

**Copilot Studio solves this by letting you build AI agents that handle these interactions automatically, 24/7, across every channel your organization uses.**

```
✅ Employee asks Teams bot: "How many leave days do I have left?"
   → Agent checks HR system → answers instantly, any time

✅ Customer chats on website: "Where is my order?"
   → Agent queries order system → gives live tracking in seconds

✅ Employee requests password reset → Agent verifies identity,
   triggers automated reset, confirms — zero human involvement
```

---

## 1.2 🧠 What Is Microsoft Copilot Studio?

**Microsoft Copilot Studio** is a **low-code platform** for building, deploying, and managing AI-powered conversational agents (also called "copilots" or "bots").

It was formerly known as **Power Virtual Agents** and was rebranded in 2023 to reflect deep integration with Microsoft's generative AI and Copilot ecosystem.

Key characteristics:

| Feature | Detail |
|---|---|
| **Builder type** | Low-code visual canvas + Power Automate + optional code |
| **AI engine** | Azure OpenAI (GPT-4), built-in NLU, generative answers |
| **Deployment** | Teams, SharePoint, web, mobile, WhatsApp, SMS, email |
| **Integration** | 1,000+ Power Platform connectors, Azure, Dataverse |
| **Governance** | DLP, AAD auth, audit logs, Purview compliance |
| **Licensing** | Microsoft 365 plans + per-session/per-message add-ons |

---

## 1.3 🗺️ The Microsoft AI Ecosystem — Where Does Copilot Studio Fit?

It helps to understand the full landscape before diving in:

```
Microsoft AI Ecosystem
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────┐
│              MICROSOFT 365 COPILOT                       │
│  Built-in AI in Word, Excel, Teams, Outlook             │
│  (Pre-built — you don't build this)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │   COPILOT STUDIO  ◄─── You are here │
          │   Build custom agents    │
          │   for YOUR use cases     │
          └────────────┬────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────┐   ┌──────────────┐  ┌──────────────┐
│  POWER   │   │    AZURE     │  │  MICROSOFT   │
│AUTOMATE  │   │  AI FOUNDRY  │  │  DATAVERSE   │
│(Actions) │   │ (Advanced AI)│  │  (Database)  │
└──────────┘   └──────────────┘  └──────────────┘
```

**Think of it this way:**
- **Microsoft 365 Copilot** = the AI assistant baked into Office apps
- **Copilot Studio** = the tool you use to BUILD your own custom AI assistants
- **Azure AI Foundry** = for data scientists building custom models from scratch
- **Power Automate** = the engine that connects your agent to real systems

---

## 1.4 ⚖️ Copilot Studio vs Other Tools — Which Should You Use?

| Tool | Best For | Requires |
|---|---|---|
| **Copilot Studio** | Business agents, M365 integration, fast delivery | Low-code skills |
| **Azure Bot Service** | Complex custom bots, full code control | C# / Node.js dev skills |
| **Azure AI Foundry** | Custom AI models, fine-tuning, advanced RAG | ML/AI expertise |
| **Power Virtual Agents** | Simple FAQ bots (older name — now Copilot Studio) | Low-code skills |
| **ChatGPT / Claude** | General AI chat — not for building custom agents | N/A |

**Rule of thumb:**
> If you work in a Microsoft 365 environment and want to deliver quickly without heavy coding — **Copilot Studio is your tool.**

---

## 1.5 💡 5 Core Concepts You Must Know

Before touching the interface, understand these 5 building blocks. Everything else will make more sense.

---

### 🟦 Concept 1: Agent (Copilot)

An **agent** is your AI assistant — the thing users talk to. It has a name, a personality, a set of skills, and knowledge it can draw from.

```
Your Agent = Name + Personality + Topics + Knowledge + Actions
Example: "TechHelp Bot" — answers IT questions and creates tickets
```

---

### 🟦 Concept 2: Topic

A **topic** is a specific conversation skill — one thing the agent knows how to handle.

```
Topics examples:
  ├── "Reset my password"        → walks user through password reset
  ├── "Check leave balance"      → queries HR system, returns result
  ├── "IT hardware request"      → collects details, creates a ticket
  └── "Greeting"                 → says hello and offers a menu
```

Each topic has a **trigger** (what activates it) and a **conversation flow** (what happens next).

---

### 🟦 Concept 3: Entity

An **entity** is a piece of information you want to extract from what the user says.

```
User says: "I need a laptop for my new team member John starting Monday"

Entities extracted:
  ├── Item:       "laptop"
  ├── Person:     "John"
  └── Date:       "Monday" → resolved to 2026-05-18
```

Entities let your agent understand context, not just keywords.

---

### 🟦 Concept 4: Variable

A **variable** stores information during a conversation — like a temporary memory.

```
Topic: IT Hardware Request

Variables used:
  {Topic.EmployeeName}    = "John"
  {Topic.ItemRequested}   = "laptop"
  {Topic.StartDate}       = "2026-05-18"
  {Global.UserDepartment} = "Engineering"    ← shared across topics

→ All passed to Power Automate to create the ticket
```

---

### 🟦 Concept 5: Action

An **action** is something the agent actually *does* — not just says.

```
Actions examples:
  ├── Call a REST API          → check order status
  ├── Run a Power Automate flow → create a Jira ticket
  ├── Query SharePoint          → search knowledge base
  ├── Send a Teams message      → notify a manager
  └── Look up Dataverse record  → fetch employee data
```

Actions are what make your agent genuinely useful, not just a fancy FAQ page.

---

## 1.6 🖥️ Setting Up Your Environment

### Step 1: Get Access

**Option A — Free Trial (Recommended for learning)**
1. Go to: [https://make.powerapps.com](https://make.powerapps.com)
2. Sign in with a Microsoft account (or create one free)
3. Start a **Copilot Studio trial** — 30 days, no credit card

**Option B — Microsoft 365 Developer Program (Best for practice)**
1. Go to: [https://developer.microsoft.com/microsoft-365/dev-program](https://developer.microsoft.com/microsoft-365/dev-program)
2. Join for free — you get a full M365 E5 sandbox with 25 user licences
3. Includes Copilot Studio access — perfect for building real scenarios

**Option C — Existing Work/School Account**
- If your org has Power Platform licences, you likely already have access
- Check with your IT admin for the correct environment

---

### Step 2: Navigate to Copilot Studio

```
Method 1: Direct URL
→ https://web.powerva.microsoft.com

Method 2: Via Power Platform
→ make.powerapps.com → left nav → "Copilot Studio"

Method 3: Via Microsoft 365
→ microsoft365.com → App Launcher (9 dots) → Copilot Studio
```

---

### Step 3: Create Your First Environment

An **environment** is like a workspace — it holds your agents, data, and settings.

```
1. Click the Environment selector (top right)
2. Click "New environment" if none exists
3. Name it: "Learning - Copilot Studio"
4. Type: Developer (for learning) or Sandbox (for team testing)
5. Region: Choose closest to your location
6. Click "Save"
```

> 💡 **Tip:** Always use a separate environment for learning — never your production environment.

---

## 1.7 🗺️ Interface Tour

Once you're in Copilot Studio, here's what you'll see:

```
┌────────────────────────────────────────────────────────┐
│  ☰  Copilot Studio         🔍 Search      👤 Account   │
├─────────────┬──────────────────────────────────────────┤
│             │                                          │
│  LEFT NAV   │           MAIN CANVAS                    │
│             │                                          │
│ 🏠 Home     │   ┌─────────────────────────────────┐   │
│ 🤖 Agents   │   │   Your Agents Dashboard         │   │
│ 🔌 Actions  │   │                                 │   │
│ 📊 Analytics│   │  + Create new agent             │   │
│ ⚙️ Settings │   │                                 │   │
│             │   │  [HR FAQ Bot]  [IT Helpdesk]    │   │
│             │   └─────────────────────────────────┘   │
└─────────────┴──────────────────────────────────────────┘
```

**Key areas to know:**

| Area | Purpose |
|---|---|
| **Home** | Dashboard, recent agents, quick actions |
| **Agents** | Create and manage all your agents |
| **Topics** (inside agent) | Design conversation flows |
| **Actions** (inside agent) | Connect to external systems |
| **Knowledge** (inside agent) | Add documents, SharePoint, websites |
| **Analytics** | Conversation volume, success rates, topics used |
| **Settings** | Authentication, channels, security |
| **Test panel** | Talk to your agent while building it |

---

## 1.8 📋 Lesson Summary

```
✅ What you now know:

  Problem solved:   AI agents handle repetitive tasks 24/7
  What it is:       Low-code platform for building custom AI agents
  Where it fits:    Between M365 Copilot (pre-built) and Azure AI (code-first)
  When to use it:   M365 environments, fast delivery, business users

  5 Core concepts:
    Agent    → the AI assistant itself
    Topic    → a conversation skill (one thing it can handle)
    Entity   → a piece of info extracted from user input
    Variable → memory stored during a conversation
    Action   → something the agent actually does

  Environment:      Set up at make.powerapps.com
```

---

## 🚀 Next Step

You understand the foundations. Now let's **build something real.**

> 👉 **[Lesson 2 — Build Your First Agent in 30 Minutes →](02-first-agent.md)**

---

*[← Back to Copilot Studio Guide](README.md)*
