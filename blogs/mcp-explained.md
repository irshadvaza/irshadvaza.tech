### 🔌 MCP — The USB-C of AI: How the Model Context Protocol Works

**Category:** AI Engineering / AI Architecture  
**Level:** Beginner → Advanced

**What you'll learn:**
- What MCP is and why Anthropic introduced it
- The USB-C analogy that makes it click instantly
- All 5 components: LLM, Client, Server, Tools, Resources
- Real-world examples across healthcare, enterprise, and data
- Step-by-step MCP setup in Microsoft Copilot / VS Code

👉 **Read Full Article:** [Open Blog](blogs/mcp-explained.md)
[Home](index.md) | [Projects](projects.md) | [Blogs](blogs.md) | [About](about.md) | [Contact](contact.md)

---

# 🔌 MCP — The USB-C of AI: How the Model Context Protocol Connects LLMs to the Real World

> **The universal connector that lets any AI talk to any tool, any database, and any API — in a standard, secure, and scalable way.**

**Category:** AI Engineering / AI Architecture  
**Level:** Beginner → Advanced  
**Author:** Irshad Vaza · AI, Data & Cloud Expert

---

## 📖 Table of Contents

1. [What Problem Does MCP Solve?](#1--what-problem-does-mcp-solve)
2. [The USB-C Analogy — Why MCP Is a Game Changer](#2--the-usb-c-analogy)
3. [What Is MCP? (Official Definition, Simply Explained)](#3--what-is-mcp)
4. [MCP Architecture: The 5 Core Components](#4--mcp-architecture-the-5-core-components)
5. [How MCP Works: Step-by-Step Flow](#5--how-mcp-works-step-by-step)
6. [Real-World Examples — Easy to Understand](#6--real-world-examples)
7. [MCP vs Traditional API Integration](#7--mcp-vs-traditional-api-integration)
8. [MCP in Microsoft Copilot — Step by Step](#8--mcp-in-microsoft-copilot)
9. [Popular MCP Servers You Can Use Today](#9--popular-mcp-servers)
10. [Should You Learn MCP?](#10--should-you-learn-mcp)

---

## 1. 🚨 What Problem Does MCP Solve?

Imagine you have a brilliant personal assistant (an AI like Claude, ChatGPT, or Copilot). They're incredibly smart — but they're locked in a room with **no phone, no computer, no access to any system**.

You ask them:

- *"What's my latest Jira ticket?"* → They can't check Jira.  
- *"Send this summary to Slack?"* → They can't reach Slack.  
- *"Pull sales data from our database?"* → No database access.

Every time you want your AI to connect to an external system, developers had to build **custom, one-off integrations** — different code for every tool, every AI model, every platform. It was messy, expensive, and didn't scale.

**MCP solves this by providing one universal standard for ALL of these connections.**

---

## 2. 🔌 The USB-C Analogy — Why MCP Is a Game Changer

Remember the chaos before USB-C? Every device had a different charger. Phone chargers, laptop chargers, camera cables — all incompatible. Then USB-C arrived: **one connector for everything**.

**MCP is the USB-C of AI.**

```
BEFORE MCP (The Old World)
──────────────────────────
Claude ──── custom code ──── Jira
Claude ──── custom code ──── Slack  
Claude ──── custom code ──── SQL DB
GPT-4 ──── different code ── Jira   ← rebuild everything!
GPT-4 ──── different code ── Slack

AFTER MCP (The New World)
──────────────────────────
Claude ──┐
GPT-4  ──┤── MCP Standard ──── Jira Server
Copilot──┘                ──── Slack Server
                          ──── SQL Server
                          ──── Any Tool...
```

> **One protocol. Any AI. Any tool. Plug and play.**

---

## 3. 🧠 What Is MCP?

**Model Context Protocol (MCP)** is an **open standard** introduced by **Anthropic in November 2024** that defines a universal way for AI language models to interact with:

- 🛠️ **Tools** (web search, code execution, calculators)
- 📂 **Resources** (files, databases, knowledge bases)
- 🌐 **APIs** (Jira, Slack, GitHub, CRM systems)
- 💬 **Prompts** (reusable AI instruction templates)

Think of it like **HTTP for the web** — HTTP standardized how browsers talk to websites. MCP standardizes how AI models talk to external systems.

| What MCP Replaces | What MCP Provides |
|---|---|
| Custom, one-off API integrations | A single universal protocol |
| Rebuild integrations for each LLM | Write once, use with any AI |
| No standard for tool communication | Clear, open specification |
| Security nightmares with ad-hoc code | Built-in safety controls |

---

## 4. 🏗️ MCP Architecture: The 5 Core Components

Understanding MCP comes down to 5 key building blocks. Let's walk through each one.

---

### 🧠 Component 1: LLM (The Brain)

The **Large Language Model** — Claude, GPT-4, Copilot, Gemini — is the thinking engine. It reads your request, decides what it needs, and calls the right tools through MCP.

```
User: "Summarize all critical bugs from Jira assigned to me this week"
  ↓
LLM thinks: "I need to query Jira. I'll use the MCP Jira Tool."
```

The LLM does NOT directly touch external systems. It communicates through the MCP layer — keeping things safe and standardized.

---

### 💻 Component 2: MCP Client (The Translator)

The **MCP Client** lives inside the AI application (Claude Desktop, VS Code, Copilot). It is the bridge between the LLM and the outside world.

**Its job:**
- Receives tool requests from the LLM
- Sends them to the correct MCP Server
- Returns results back to the LLM

```
AI App (Claude / Copilot)
  └── MCP Client
        ├── Connects to: Jira MCP Server
        ├── Connects to: Slack MCP Server
        └── Connects to: Database MCP Server
```

Think of the MCP Client as a **universal remote control** that can talk to any MCP-compatible device.

---

### 🖥️ Component 3: MCP Server (The Worker)

The **MCP Server** is a lightweight program that wraps around an external tool or API and exposes it in a standard MCP format.

Each MCP Server exposes:
- **What it can do** (list of available tools)
- **How to call it** (input/output format)
- **What data it has** (resources)

```
Jira MCP Server
  ├── Tool: get_my_issues()
  ├── Tool: create_ticket(title, description)
  ├── Tool: update_status(ticket_id, status)
  └── Resource: project_list
```

MCP Servers are the "adapters" — like the USB-C adapter that makes your old HDMI screen work with your new MacBook.

---

### 🛠️ Component 4: Tools (The Actions)

**Tools** are specific functions that an MCP Server exposes — things the AI can *do*:

| Tool Example | What It Does |
|---|---|
| `search_web(query)` | Search the internet |
| `run_sql(query)` | Execute a database query |
| `send_slack_message(channel, text)` | Post to Slack |
| `create_jira_ticket(...)` | Create a new Jira issue |
| `read_file(path)` | Read a file from disk |
| `call_api(endpoint, params)` | Call any REST API |

Tools are the **verbs** — the actions the AI can perform in the real world.

---

### 📚 Component 5: Resources & Prompts

**Resources** are data sources the AI can read — like files, database records, or documents. They're the **nouns** — the things the AI can know about.

**Prompts** are reusable instruction templates stored in an MCP Server — like saved command recipes. Example:

```
Prompt: "daily_standup_summary"
→ "Fetch my Jira tickets updated in last 24hrs, 
   check Slack for unread mentions, 
   and write a 5-bullet standup summary."
```

One command triggers a multi-step AI workflow — automatically.

---

## 5. ⚙️ How MCP Works: Step-by-Step

Here is the complete flow of an MCP interaction:

```
Step 1: User sends a request
────────────────────────────
User → "What are my open Jira tickets due this week?"

Step 2: LLM understands and decides
────────────────────────────────────
LLM → "I need to use the Jira tool: get_my_issues(due=this_week)"

Step 3: MCP Client sends the request
──────────────────────────────────────
MCP Client → sends JSON request to Jira MCP Server

Step 4: MCP Server executes the action
────────────────────────────────────────
Jira MCP Server → calls Jira REST API → gets ticket data

Step 5: Result flows back to LLM
──────────────────────────────────
Jira API → MCP Server → MCP Client → LLM

Step 6: LLM crafts the response
──────────────────────────────────
LLM → "You have 3 open tickets due this week:
       1. PROJ-101: Fix login bug (High Priority)
       2. PROJ-87: Update dashboard (Medium)
       3. PROJ-112: Code review (Low)"

Step 7: User gets a human answer
──────────────────────────────────
Response displayed to User ✅
```

All of this happens in seconds. The user just asked a question in plain English.

---

## 6. 🌍 Real-World Examples — Easy to Understand

### 🏥 Example 1: Healthcare Assistant

**Without MCP:** A hospital AI chatbot can only answer from its training data. It has no live patient info.

**With MCP:**
```
Doctor: "Summarize patient John's last 3 lab results and flag anything abnormal."

MCP Flow:
  AI → [EMR MCP Server] → fetches lab records from hospital system
  AI → [Guidelines MCP Server] → checks clinical guidelines
  AI → generates structured summary with flagged anomalies

Result: Doctor gets a real-time, accurate clinical summary in seconds.
```

---

### 🏢 Example 2: Enterprise Employee Assistant

**Scenario:** An employee asks their AI assistant a complex question.

```
Employee: "Book a meeting with the sales team for next Tuesday 
           and create a Jira ticket for the follow-up actions 
           we discussed in today's Teams call."

MCP Flow:
  AI → [Calendar MCP Server]  → checks availability, books meeting
  AI → [Teams MCP Server]     → retrieves transcript of today's call
  AI → [Jira MCP Server]      → creates tickets from action items

Result: Three systems updated, automatically, from one sentence.
```

---

### 📊 Example 3: Data Analyst Copilot

```
Analyst: "Show me last month's revenue by region 
          and compare it to the same period last year."

MCP Flow:
  AI → [SQL MCP Server]      → runs query on data warehouse
  AI → [Charts MCP Server]   → generates visualization
  AI → [Report MCP Server]   → formats into slide-ready output

Result: Complete analysis with charts, ready in 10 seconds.
```

---

### 🛒 Example 4: E-commerce Operations Bot

```
Manager: "Which products had returns above 5% last week? 
          Email the suppliers for the top 3 items."

MCP Flow:
  AI → [Database MCP Server] → queries returns data
  AI → [CRM MCP Server]      → fetches supplier contact info
  AI → [Email MCP Server]    → drafts and sends professional emails

Result: A task that used to take 30 minutes is done in 30 seconds.
```

---

## 7. ⚖️ MCP vs Traditional API Integration

| Factor | Traditional API | MCP Standard |
|---|---|---|
| Integration effort | High — custom code per tool | Low — one standard for all |
| AI model switching | Rebuild everything | Plug in any MCP-compatible AI |
| Security model | Ad-hoc per integration | Built-in, standardized controls |
| Discovery | Manual documentation | AI auto-discovers available tools |
| Maintenance | Update each integration separately | Update MCP Server once |
| Time to integrate new tool | Days to weeks | Hours |
| Vendor lock-in | High | None — open standard |

**Bottom line:** MCP turns months of custom integration work into a plug-and-play ecosystem.

---

## 8. 🤖 MCP in Microsoft Copilot — Step by Step

Microsoft Copilot now supports MCP, making it possible to extend Copilot with any MCP Server. Here's how to set it up and use it.

---

### 🔷 Step 1: Understand What's Available

Microsoft has integrated MCP support into:
- **Microsoft 365 Copilot** (Word, Excel, Teams, Outlook)
- **GitHub Copilot** (VS Code, JetBrains)
- **Copilot Studio** (custom enterprise agents)
- **Azure AI Foundry** (advanced enterprise deployments)

---

### 🔷 Step 2: Enable MCP in GitHub Copilot (VS Code)

This is the easiest way to get started with MCP today.

**Prerequisites:**
- VS Code installed
- GitHub Copilot subscription (Individual, Business, or Enterprise)
- VS Code version 1.99 or later

**Step-by-step:**

```bash
# Step 1: Open VS Code
# Step 2: Go to Settings → search for "MCP"
# Step 3: Enable: "Chat > MCP: Enabled"

# Step 4: Create your MCP config file
# Location: .vscode/mcp.json  (project level)
# OR: ~/.config/github-copilot/mcp.json  (global)
```

**Example mcp.json — Adding a File System MCP Server:**

```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/Documents/projects"
      ]
    }
  }
}
```

**What this does:** GitHub Copilot can now read, search, and reference files in your projects folder — directly in chat.

---

### 🔷 Step 3: Add a Database MCP Server

```json
{
  "servers": {
    "postgres-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

Now you can ask Copilot in VS Code:
> *"Show me all orders from last week where total > $1000"*

Copilot will write AND execute the SQL — returning live results.

---

### 🔷 Step 4: Add GitHub MCP Server

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

Now ask Copilot:
> *"List all open PRs in my repo that haven't been reviewed in 3 days"*
> *"Create a new issue titled 'Fix memory leak in auth module'"*

---

### 🔷 Step 5: Use MCP in Copilot Studio (Enterprise)

For Microsoft 365 Copilot in enterprise environments, use **Copilot Studio** to register MCP Servers as connectors.

```
Copilot Studio → Agents → Create Agent
  → Add Action → Connect MCP Server
  → Enter: MCP Server URL + Authentication
  → Publish to Microsoft 365 Copilot
```

**Example enterprise use case:**

```
Employee in Teams: "Raise a support ticket for the network outage 
                   in our Dubai office and notify the IT team lead."

Copilot (via MCP):
  → [ServiceNow MCP] creates incident ticket
  → [Azure AD MCP]  looks up IT team lead contact
  → [Teams MCP]     sends notification message

All done from one Teams message.
```

---

### 🔷 Step 6: Verify MCP is Working

In VS Code with GitHub Copilot:

```
1. Open Copilot Chat panel (Ctrl+Shift+I)
2. Type: @  — you should see your MCP tools listed
3. Or simply ask a question that requires your tool
4. Copilot will ask permission before calling any MCP tool ✅
```

**Security note:** Copilot always shows you which MCP tool it wants to call and asks for confirmation before executing. You stay in control.

---

## 9. 🌐 Popular MCP Servers You Can Use Today

The MCP ecosystem is growing rapidly. Here are production-ready servers:

| MCP Server | What It Does | Use Case |
|---|---|---|
| `@mcp/server-filesystem` | Read/write local files | Document analysis, code review |
| `@mcp/server-github` | GitHub repos, PRs, issues | Dev workflows, code automation |
| `@mcp/server-postgres` | PostgreSQL queries | Data analysis, reports |
| `@mcp/server-slack` | Read/send Slack messages | Team communication |
| `@mcp/server-brave-search` | Web search via Brave | Research, current events |
| `@mcp/server-puppeteer` | Web scraping, browser automation | Data collection |
| `@mcp/server-azure` | Azure resource management | Cloud ops |
| `mcp-server-jira` | Jira tickets and projects | Agile workflows |
| `mcp-server-servicenow` | ITSM operations | Enterprise IT |
| `mcp-server-salesforce` | CRM data and workflows | Sales automation |

> 📦 **Browse all MCP Servers:** [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers)  
> 🏪 **GitHub MCP Registry:** [github.com/mcp](https://github.com/mcp)

---

## 10. 🎯 Should You Learn MCP?

### ✅ Yes, if you are a...

| Role | Why MCP Matters to You |
|---|---|
| **AI Engineer** | Build production AI agents that actually do things |
| **Data Engineer** | Connect AI to your data platforms without custom glue code |
| **Enterprise Architect** | Design governed, scalable AI integration layers |
| **Developer** | Extend any AI tool with your own services |
| **IT Leader** | Understand the standard that will power enterprise AI in 2025+ |

### 🚀 What MCP Enables in 2025 and Beyond

- **Agentic AI** — AI that takes real actions, not just answers questions
- **Multi-agent systems** — AI agents collaborating through shared MCP tools
- **Enterprise AI fabric** — one standard connecting all enterprise systems to AI
- **No more vendor lock-in** — switch AI models while keeping all integrations

---

## 🗺️ MCP Learning Roadmap

```
🟢 BEGINNER
  └── Understand what MCP is (this article ✅)
  └── Install Claude Desktop + one MCP Server
  └── Try: filesystem or SQLite MCP with Claude

🟡 INTERMEDIATE
  └── Add MCP to GitHub Copilot in VS Code
  └── Connect to a real database via MCP
  └── Build your first custom MCP Server (Python/Node.js)

🔵 ADVANCED
  └── Design enterprise MCP architecture
  └── Build multi-tool AI agents
  └── Deploy MCP in Microsoft Copilot Studio
  └── Implement MCP security & governance patterns
```

---

## 📋 Quick Reference Card

```
MCP in One Page
═══════════════════════════════════════════════════

What is MCP?    → Universal standard for AI ↔ Tool communication
Who made it?    → Anthropic (Nov 2024), now open standard
Analogy?        → USB-C for AI applications

5 Components:
  1. LLM         → The AI brain (Claude, GPT-4, Copilot)
  2. MCP Client  → Bridge inside the AI app
  3. MCP Server  → Adapter wrapping an external tool/API
  4. Tools       → Actions the AI can perform
  5. Resources   → Data the AI can read

Key Benefits:
  ✅ Write once, use with any AI model
  ✅ Open standard — no vendor lock-in
  ✅ Built-in security and permission controls
  ✅ Massive ecosystem of ready-made servers

Where to start?
  → GitHub Copilot + VS Code (easiest)
  → Claude Desktop (most powerful)
  → Copilot Studio (enterprise)

Registry: github.com/mcp
Docs:     modelcontextprotocol.io
```

---

## 🔗 Resources & Next Steps

- 📘 **Official MCP Docs:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- 🏪 **MCP Server Registry:** [github.com/mcp](https://github.com/mcp)
- 🔵 **Microsoft Copilot MCP Guide:** [Microsoft Learn — MCP in Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/mcp)
- ⚡ **Claude + MCP Setup:** [Anthropic MCP Quickstart](https://modelcontextprotocol.io/quickstart)
- 🧪 **Try MCP Inspector:** Test your MCP servers visually

---

## 🔗 Connect & Explore

- 💻 GitHub: [github.com/irshadvaza](https://github.com/irshadvaza)
- 📊 Kaggle: [kaggle.com/irshadvaza](https://www.kaggle.com/code/irshadvaza)
- 🌐 Portfolio: [Back to Home](index.md) | [More Blogs](blogs.md)

---

> **MCP is not just a technical standard — it is the foundation of the agentic AI era. The AI models that will matter most are not the ones that know the most, but the ones that can *do* the most. MCP makes that possible.**

---

*Written by Irshad Vaza — AI, Data & Cloud Architect | May 2025*
