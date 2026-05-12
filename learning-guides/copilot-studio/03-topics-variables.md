[Home](../../index.md) | [Learning Guides](../README.md) | [Copilot Studio](README.md) | [← Lesson 2](02-first-agent.md) | [Lesson 4 →](04-connectors-actions.md)

---

# 🧠 Lesson 3 — Conversations, Topics & Variables

> **The difference between a frustrating bot and a great AI agent is conversation design. Master it here.**

**⏱ Time:** 90 minutes &nbsp;|&nbsp; **Level:** 🟡 Intermediate &nbsp;|&nbsp; **Prerequisites:** Lessons 1–2

---

## 📋 What You'll Build

A **Smart IT Helpdesk Agent** with:
- Dynamic troubleshooting paths based on issue type
- Slot filling (collecting multiple pieces of info naturally)
- Global variables (memory shared across topics)
- Adaptive cards for rich, visual responses
- Graceful fallback with escalation to a human

---

## 📋 What You'll Learn

- [ ] Topic types and when to use each
- [ ] Trigger phrases — quality over quantity
- [ ] All 8 conversation node types
- [ ] Entities — built-in and custom
- [ ] Variables — topic, global, and system scope
- [ ] Slot filling — collecting info conversationally
- [ ] Branching logic with conditions
- [ ] Redirection between topics
- [ ] Escalation to human agents

---

## 3.1 🧩 Topic Types — Not All Topics Are Equal

Copilot Studio has three types of topics. Understanding when to use each is key.

```
┌─────────────────────────────────────────────────────────┐
│  SYSTEM TOPICS (built-in, always present)               │
│  ├── Greeting          → first message from user        │
│  ├── Goodbye           → ending the conversation        │
│  ├── Escalate          → user wants a human             │
│  ├── Start over        → user wants to restart          │
│  └── Fallback          → agent doesn't understand       │
├─────────────────────────────────────────────────────────┤
│  CUSTOM TOPICS (you build these)                        │
│  ├── Information topics  → answer questions             │
│  ├── Task topics         → do something (collect info)  │
│  └── Triage topics       → figure out what user needs   │
├─────────────────────────────────────────────────────────┤
│  LESSON TOPICS (built-in samples you can learn from)    │
│  └── Example flows Microsoft provides                   │
└─────────────────────────────────────────────────────────┘
```

> **Best practice for IT Helpdesk:** Build one **Triage topic** that asks what the issue is about, then **redirects** to specialized topics. This is cleaner than one giant topic trying to do everything.

---

## 3.2 🎯 Trigger Phrases — The Science of Getting Them Right

This is where most beginners go wrong. Here's the framework:

### ❌ Common mistakes:

```
Too similar (redundant):
  • "I need help"
  • "Can I get help"
  • "Help me please"
  → AI sees these as the same → wastes your phrase budget

Too broad (triggers wrong topic):
  • "Problem"   ← could mean anything
  • "Issue"     ← too vague
  • "Help"      ← conflicts with every other topic
```

### ✅ Best practice:

```
Cover different INTENTS, not different WORDINGS of the same intent:
  • "My laptop won't turn on"              ← hardware failure
  • "I can't connect to the VPN"           ← network issue
  • "Password reset"                       ← access issue
  • "Software not working"                 ← application issue
  • "Computer is very slow"               ← performance issue

Aim for 5–8 high-quality, distinct phrases per topic.
The AI NLU handles the variations — you handle the intent coverage.
```

---

## 3.3 🗂️ All 8 Conversation Node Types

Open any topic in the canvas — click "+" to see every node type available. Here's what each one does:

| Node | Icon | Purpose | When to Use |
|---|---|---|---|
| **Send a message** | 💬 | Display text, images, tables | Any response to the user |
| **Ask a question** | ❓ | Collect info from user | When you need specific input |
| **Add a condition** | 🔀 | Branch the conversation | Different paths for different users |
| **Variable management** | 📦 | Set/clear variables | Store or reset data mid-conversation |
| **Topic management** | ↩️ | Go to another topic | Redirect, end, or start over |
| **Call an action** | ⚡ | Run Power Automate, connectors | When the agent needs to DO something |
| **Send an adaptive card** | 🃏 | Rich visual UI components | Forms, buttons, images, tables |
| **Generative answers** | 🤖 | AI answer from knowledge | When topic doesn't have a set answer |

---

## 3.4 🏷️ Entities — Teaching the Agent What Things Mean

Entities let the agent understand the *type* of information in what the user says.

### Built-in entities (ready to use):

```
Entity Type        Example user input         What's extracted
──────────────────────────────────────────────────────────────
📅 Date & Time     "next Monday at 3pm"    →  2026-05-18T15:00
📧 Email           "send to bob@co.com"    →  bob@co.com
🔢 Number          "I have 3 monitors"     →  3
📞 Phone           "call 04-123-4567"      →  04-123-4567
⏱️ Duration        "for the next 2 weeks"  →  14 days
🌍 Geography       "in the Dubai office"   →  Dubai
✅ Boolean         "yes please"            →  true
```

### Creating a custom entity:

For IT Helpdesk, create an **"IssueType"** entity:

```
1. Go to Settings → Entities → "+ New entity"
2. Name: IssueType
3. Type: Closed list
4. Add values:
   ├── Hardware     (synonyms: laptop, computer, monitor, mouse, keyboard)
   ├── Software     (synonyms: app, application, program, Excel, Teams)
   ├── Network      (synonyms: WiFi, internet, VPN, connectivity, slow)
   ├── Access       (synonyms: password, login, account, locked out, permissions)
   └── Other
5. Save
```

Now when a user says *"I can't open Excel"* the agent automatically extracts `IssueType = Software`.

---

## 3.5 📦 Variables — The Agent's Memory

Variables store information during (and across) conversations. There are three scopes:

```
┌─────────────────────────────────────────────────────────┐
│  TOPIC VARIABLES   {Topic.VariableName}                  │
│  ─────────────────────────────────────────────────────  │
│  • Exist only within the current topic                  │
│  • Created automatically when you save a question answer │
│  • Cleared when the topic ends                          │
│                                                         │
│  Example: {Topic.IssueType} = "Hardware"                │
├─────────────────────────────────────────────────────────┤
│  GLOBAL VARIABLES  {Global.VariableName}                 │
│  ─────────────────────────────────────────────────────  │
│  • Persist across ALL topics in the conversation         │
│  • Must be explicitly created in Settings               │
│  • Perfect for: user name, department, ticket number    │
│                                                         │
│  Example: {Global.UserEmail} = "ahmed@contoso.com"      │
├─────────────────────────────────────────────────────────┤
│  SYSTEM VARIABLES  {System.VariableName}                 │
│  ─────────────────────────────────────────────────────  │
│  • Auto-populated by Copilot Studio                     │
│  • Read-only                                            │
│                                                         │
│  Examples:                                              │
│    {System.User.DisplayName} = "Ahmed Al-Rashidi"       │
│    {System.User.Email}       = "ahmed@contoso.com"      │
│    {System.Conversation.Id}  = "conv_abc123"            │
└─────────────────────────────────────────────────────────┘
```

### Setting up a Global Variable:

```
1. Go to Settings (inside the agent) → Variables
2. Click "+ New variable"
3. Name: UserDepartment
4. Type: String
5. Default value: (leave blank — set during conversation or auth)
```

---

## 3.6 🏗️ Build the IT Helpdesk Agent — Triage Topic

Create a new agent: **IT Helpdesk**

Then create the main triage topic:

**Topic name:** `IT Support - Main Menu`

**Trigger phrases:**
```
• IT support
• I have a technical problem
• Help with my computer
• Tech issue
• Something isn't working
• I need IT help
• Technical support request
```

**Conversation flow:**

```
[Message node]
"Hi {System.User.DisplayName}! 👋 I'm the IT Support assistant.

I can help you with hardware, software, network, and access issues.

Let's get started — what type of issue are you experiencing?"

[Ask a question node]
Question: What category best describes your issue?
Answer type: Multiple choice options

Options:
  💻 Hardware (laptop, monitor, printer)
  🖥️ Software (apps, Office, Teams)
  🌐 Network (WiFi, VPN, internet)
  🔐 Access (password, account locked)
  ❓ Something else

Save to variable: Topic.IssueCategory
```

Then add **conditions** (Add a condition node):

```
Condition 1: Topic.IssueCategory is equal to "💻 Hardware"
  → Go to Topic: "Hardware Troubleshooting"

Condition 2: Topic.IssueCategory is equal to "🖥️ Software"  
  → Go to Topic: "Software Troubleshooting"

Condition 3: Topic.IssueCategory is equal to "🌐 Network"
  → Go to Topic: "Network Troubleshooting"

Condition 4: Topic.IssueCategory is equal to "🔐 Access"
  → Go to Topic: "Access & Password Reset"

All other conditions (else):
  → Message: "Let me connect you to an IT agent who can help."
  → Go to Topic: "Escalate" (system topic)
```

---

## 3.7 🏗️ Build the Hardware Troubleshooting Topic

**Topic name:** `Hardware Troubleshooting`

**No trigger phrases** — this topic is always reached by redirect, not by user typing.

**Flow:**

```
[Message] 
"Let's troubleshoot your hardware issue. I'll ask a few quick questions."

[Ask a question]
"What's happening with your hardware?"
Options:
  • Won't turn on / not starting
  • Running very slowly
  • Screen / display problem
  • Keyboard or mouse issue
  • Something else

Save to: Topic.HardwareIssue

─── Branch: "Won't turn on" ───────────────────────────────

[Message]
"🔌 Let's try these steps first:

**Step 1:** Hold the power button for 10 seconds to force off
**Step 2:** Unplug all cables and remove the power adapter
**Step 3:** Wait 30 seconds
**Step 4:** Plug back in and try powering on

Did that fix the issue?"

[Ask question] → Yes / No

  If YES: "Great! If it happens again, contact IT so we can run diagnostics."
  If NO:  → Collect info and escalate (see below)

─── Escalation flow ────────────────────────────────────────

[Ask question]
"I'll need to raise a ticket for you. What's your employee ID?"
Save to: Topic.EmployeeID

[Ask question]
"Please briefly describe what you're experiencing:"
Save to: Topic.IssueDescription

[Variable management]
Set Global.TicketDetails = "{Topic.HardwareIssue} - {Topic.IssueDescription}"

[Message]
"✅ Got it. I've collected your details:

Employee ID: {Topic.EmployeeID}
Issue: {Topic.IssueDescription}

📋 Next: I'll create a support ticket for you.
⏱️ An IT engineer will contact you within 2 business hours.

Your reference: IT-{System.Conversation.Id}"

[End with survey: "Was this helpful?"]
```

> In Lesson 4, we'll replace the "I'll create a ticket" message with an **actual ticket creation** via Power Automate.

---

## 3.8 🎴 Slot Filling — Collecting Info Naturally

Slot filling lets the agent collect multiple pieces of information in a single exchange — even when the user gives them all at once.

**Example — without slot filling:**

```
Agent: What's your name?
User:  John
Agent: What's your department?
User:  Engineering
Agent: What's your issue?
User:  Laptop won't start
```

**Example — with slot filling:**

```
User:  "I'm John from Engineering and my laptop won't start"

Agent: [Extracts automatically]
  {Topic.UserName}   = "John"
  {Topic.Department} = "Engineering"  
  {Topic.Issue}      = "laptop won't start"
  
Agent: "Got it John! Let me help you with your laptop."
```

**How to enable it:**

```
1. In your Ask a Question node, enable "Slot filling"
2. Map each slot to an entity type
3. The agent will only ask for missing slots

Example slot setup for ticket creation:
  Slot 1: Employee name     → Text entity
  Slot 2: Department        → Custom "Department" entity
  Slot 3: Issue type        → Custom "IssueType" entity
  Slot 4: Priority          → Closed list: Low, Medium, High, Critical
```

---

## 3.9 ↩️ Topic Redirection & End Conditions

When a topic finishes, you control what happens next.

```
End options available in Topic Management node:

┌─────────────────────────────────────────────────────────┐
│  End conversation     → closes session (say goodbye)    │
│  Go to another topic  → redirect to a specific topic    │
│  Transfer to agent    → escalate to human (Teams, etc.) │
│  Ask again            → loop back to start of topic     │
│  End with survey      → ask "Was this helpful?" 1–5 ⭐  │
└─────────────────────────────────────────────────────────┘
```

**Best practice — always end with a choice:**

```
[Message]
"Is there anything else I can help you with?"

[Ask question]
Options:
  [Yes, I have another issue] → Go to: IT Support Main Menu
  [No, I'm all done]          → End with survey
```

---

## 3.10 🛟 Customize the Fallback Topic

The Fallback topic is what runs when the agent doesn't understand. Make it genuinely helpful:

```
1. Topics → System → Fallback → Edit

Replace the default message with:

"I'm not sure I understood that. 🤔

Let me suggest some options:
• 💻 Hardware issues
• 🖥️ Software problems  
• 🌐 Network / VPN help
• 🔐 Password / account access

Or you can:
📧 Email: itsupport@contoso.com
📞 Call: ext. 3000

Would you like to try again?"

[Ask question]
  [Try again]         → Go to: IT Support Main Menu
  [Contact IT team]   → Message with contact details + end
```

---

## 3.11 📋 Lesson Summary

```
✅ What you built:
  IT Helpdesk Agent with:
    ✅ Triage topic (main menu with category routing)
    ✅ Hardware troubleshooting with step-by-step guidance
    ✅ Slot filling for natural info collection
    ✅ Global variable for cross-topic data
    ✅ Graceful fallback with real options
    ✅ Proper end conditions with survey

✅ What you learned:
  Topic types         → system, custom, lesson
  Trigger phrases     → quality intent coverage (5-8 phrases)
  8 node types        → message, question, condition, variable, 
                        topic mgmt, action, adaptive card, generative
  Entities            → built-in + custom closed lists
  Variables           → topic, global, system scope
  Slot filling        → natural multi-slot collection
  Branching           → conditions and redirects
  Fallback            → make it genuinely helpful
```

---

## 🚀 Next Step

Your agent has great conversations. Now let's make it **actually do things** — create tickets, check live data, send notifications.

> 👉 **[Lesson 4 — Connectors, APIs & Power Automate →](04-connectors-actions.md)**

---

*[← Lesson 2: First Agent](02-first-agent.md) | [Back to Copilot Studio Guide](README.md)*
