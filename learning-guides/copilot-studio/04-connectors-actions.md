[Home](../../index.md) | [Learning Guides](../README.md) | [Copilot Studio](README.md) | [← Lesson 3](03-topics-variables.md) | [Lesson 5 →](05-generative-ai-knowledge.md)

---

# 🔌 Lesson 4 — Connectors, APIs & Power Automate

> **An agent that only talks is a fancy FAQ. An agent that acts is a productivity superpower.**

**⏱ Time:** 2 hours &nbsp;|&nbsp; **Level:** 🟡 Intermediate &nbsp;|&nbsp; **Prerequisites:** Lessons 1–3

---

## 📋 What You'll Build

An **IT Operations Agent** that:
- Creates real ServiceNow tickets via REST API
- Checks live system status from a web API
- Sends a Teams notification to the IT manager
- Looks up employee data from SharePoint

All triggered by a natural conversation — the user just describes their problem.

---

## 📋 What You'll Learn

- [ ] The three ways to connect agents to external systems
- [ ] Using built-in Power Platform connectors (SharePoint, Teams, Outlook)
- [ ] Building a Power Automate flow from Copilot Studio
- [ ] Calling REST APIs with HTTP connectors
- [ ] Passing variables in and out of flows
- [ ] Error handling and fallback strategies
- [ ] Authentication patterns (API Key, OAuth, Azure AD)

---

## 4.1 🗺️ Three Ways to Connect Your Agent to the World

```
┌─────────────────────────────────────────────────────────────┐
│  METHOD 1: Built-in Connectors (Easiest)                     │
│  ─────────────────────────────────────────────────────────  │
│  1,000+ pre-built connectors in Power Platform              │
│  Examples: SharePoint, Teams, Outlook, Dataverse            │
│  No code needed — just configure and use                    │
│  Best for: Microsoft 365 data                               │
├─────────────────────────────────────────────────────────────┤
│  METHOD 2: Power Automate Flows (Most Common)                │
│  ─────────────────────────────────────────────────────────  │
│  Build flows visually in Power Automate                     │
│  Call them from your agent as "actions"                     │
│  Combine multiple connectors in one flow                    │
│  Best for: Multi-step workflows, complex logic              │
├─────────────────────────────────────────────────────────────┤
│  METHOD 3: Custom HTTP Connector (Most Powerful)             │
│  ─────────────────────────────────────────────────────────  │
│  Call any REST API directly                                 │
│  Full control over request/response                         │
│  Build your own connector for internal APIs                 │
│  Best for: Internal systems, third-party APIs               │
└─────────────────────────────────────────────────────────────┘
```

---

## 4.2 🏗️ Method 1 — SharePoint Lookup (Employee Directory)

Let's add a live employee lookup from SharePoint to your IT Helpdesk agent.

### Prerequisites:
- A SharePoint list named `IT_Employees` with columns: `EmployeeID`, `Name`, `Department`, `Manager`, `Equipment`

### Step 1: Create the Action in Copilot Studio

```
1. Open your IT Helpdesk agent
2. Go to Actions (left nav) → + Add action
3. Search for "SharePoint" → "Get items"
4. Configure:
   Site: https://contoso.sharepoint.com/sites/IT
   List: IT_Employees
   Filter: EmployeeID eq '{Topic.EmployeeID}'
5. Outputs: Name, Department, Manager
6. Save the action as: "Lookup Employee"
```

### Step 2: Use it in a Topic

In your Hardware Troubleshooting topic, after collecting the EmployeeID:

```
[Call action: "Lookup Employee"]
  Input:  Topic.EmployeeID
  Output: Store results in Topic.EmployeeName, Topic.Manager

[Message]
"Thanks {Topic.EmployeeName}! 
I'll also notify your manager {Topic.Manager} about this issue."
```

---

## 4.3 🏗️ Method 2 — Power Automate Flow (Ticket Creation)

This is the most important skill. Let's build a flow that creates a ticket, sends a Teams message, and returns a ticket number.

### Step 1: Create the Flow from Copilot Studio

```
1. In your IT Helpdesk agent → Actions → + Add action
2. Choose "New Power Automate flow"
3. This opens Power Automate with a template:
   "Run a flow from Copilot" trigger (already added)
```

### Step 2: Define Input Parameters

In the trigger node, add these inputs that the agent will send to the flow:

```
Input parameters (add each one):
  ├── EmployeeID       (text)
  ├── EmployeeName     (text)
  ├── Department       (text)
  ├── IssueCategory    (text)
  ├── IssueDescription (text)
  └── Priority         (text)
```

### Step 3: Build the Flow Actions

Add these actions to the flow:

```
Action 1: Initialize variable
  Name: TicketNumber
  Value: IT-[utcNow('yyyyMMdd')]-[rand(1000,9999)]
  → Creates: IT-20260512-4782

Action 2: Send an HTTP request (ServiceNow API)
  Method: POST
  URI: https://your-instance.service-now.com/api/now/table/incident
  Headers:
    Content-Type: application/json
    Authorization: Basic [base64 credentials]
  Body:
    {
      "short_description": "@{triggerBody()['IssueDescription']}",
      "category": "@{triggerBody()['IssueCategory']}",
      "priority": "@{triggerBody()['Priority']}",
      "caller_id": "@{triggerBody()['EmployeeID']}",
      "description": "Created by IT Copilot Agent. Employee: @{triggerBody()['EmployeeName']}, Dept: @{triggerBody()['Department']}"
    }

Action 3: Post a message in Teams
  Team: IT Operations
  Channel: #support-alerts
  Message:
    🆕 **New IT Ticket Created**
    
    👤 Employee: @{triggerBody()['EmployeeName']} (@{triggerBody()['Department']})
    🏷️ Category: @{triggerBody()['IssueCategory']}
    🔴 Priority: @{triggerBody()['Priority']}
    📝 Issue: @{triggerBody()['IssueDescription']}
    🎫 Ticket: @{variables('TicketNumber')}

Action 4: Send an email (Outlook)
  To: @{triggerBody()['EmployeeID']}@contoso.com
  Subject: IT Support Ticket Created — @{variables('TicketNumber')}
  Body:
    Hi @{triggerBody()['EmployeeName']},
    
    Your IT support ticket has been created successfully.
    
    Ticket Number: @{variables('TicketNumber')}
    Issue: @{triggerBody()['IssueDescription']}
    Priority: @{triggerBody()['Priority']}
    
    An IT engineer will contact you within 2 business hours.
    
    IT Support Team

Action 5: Return value(s) to the agent
  TicketNumber: @{variables('TicketNumber')}
```

### Step 4: Save and Return to Copilot Studio

```
1. Name the flow: "IT - Create Support Ticket"
2. Save and publish the flow
3. Return to Copilot Studio — the flow now appears as an action
```

### Step 5: Use the Flow in Your Topic

Replace the placeholder message in your Hardware topic:

```
[Call action: "IT - Create Support Ticket"]
  Inputs:
    EmployeeID       → Topic.EmployeeID
    EmployeeName     → Topic.EmployeeName
    Department       → Global.UserDepartment
    IssueCategory    → Topic.IssueCategory
    IssueDescription → Topic.IssueDescription
    Priority         → Topic.Priority
  
  Output:
    TicketNumber → Topic.TicketNumber

[Message]
"✅ Your ticket has been created!

🎫 **Ticket Number:** {Topic.TicketNumber}
📧 A confirmation has been sent to your email
🔔 Your IT manager has been notified in Teams

⏱️ Expected response time: within 2 business hours

Is there anything else I can help you with?"
```

---

## 4.4 🏗️ Method 3 — REST API Call (System Status Check)

Let's build a topic that checks live system status from a public or internal API.

**Scenario:** Before troubleshooting, check if the reported system is already down.

### Step 1: Create a Power Automate Flow for API Call

```
Flow name: "IT - Check System Status"

Trigger: Run a flow from Copilot
  Input: SystemName (text)

Action: HTTP
  Method: GET
  URI: https://status.contoso.com/api/v1/systems/@{triggerBody()['SystemName']}
  Headers:
    Authorization: Bearer [your-api-key]
    Content-Type: application/json

Action: Parse JSON
  Content: HTTP body
  Schema: 
    {
      "type": "object",
      "properties": {
        "status": {"type": "string"},
        "last_incident": {"type": "string"},
        "uptime_percent": {"type": "number"}
      }
    }

Action: Return values to agent
  SystemStatus:     body('Parse_JSON')?['status']
  LastIncident:     body('Parse_JSON')?['last_incident']
  UptimePercent:    body('Parse_JSON')?['uptime_percent']
```

### Step 2: Use Status Check in Network Troubleshooting Topic

```
[Message]
"Let me check if there's a known issue first..."

[Call action: IT - Check System Status]
  Input: Topic.SystemName
  Output: Topic.SystemStatus, Topic.LastIncident

[Condition]
IF Topic.SystemStatus equals "operational":
  → "Good news — {Topic.SystemName} is fully operational (uptime: {Topic.UptimePercent}%).
     The issue might be local to your device. Let's troubleshoot."
  → [Continue troubleshooting flow]

IF Topic.SystemStatus equals "degraded":
  → "⚠️ {Topic.SystemName} is currently experiencing issues.
     Last incident: {Topic.LastIncident}
     Our team is already working on it. No action needed from you.
     Expected resolution: check status.contoso.com for updates."

IF Topic.SystemStatus equals "outage":
  → "🔴 {Topic.SystemName} is currently DOWN.
     Incident reported at: {Topic.LastIncident}
     Our engineers are actively resolving this.
     You'll receive an email when service is restored."
```

---

## 4.5 🔐 Authentication Patterns

Connecting to real systems requires authentication. Here are the patterns used in enterprise:

### Pattern 1: API Key (simplest)

```
Store API keys in Power Automate as environment variables:
  Settings → Environment Variables → + New
  Name: ServiceNow_API_Key
  Type: Secret

Use in HTTP action:
  Headers → Authorization: Bearer @{parameters('ServiceNow_API_Key')}
```

### Pattern 2: Azure AD (for Microsoft services)

```
Most Microsoft connectors (SharePoint, Teams, Outlook) use:
  → Sign-in with your Azure AD account in Power Automate
  → Connector handles tokens automatically
  → No keys to manage
```

### Pattern 3: OAuth2 (third-party APIs)

```
For Jira, Salesforce, ServiceNow with OAuth:
  1. Power Automate → Custom connectors → + New connector
  2. Security tab → OAuth 2.0
  3. Enter: Client ID, Client Secret, Auth URL, Token URL
  4. Define scopes needed
  5. Test the connection
```

### Pattern 4: Service Account (enterprise)

```
For internal systems:
  → Create a dedicated service account (not a personal account)
  → Grant it only the permissions the agent needs
  → Store credentials in Azure Key Vault
  → Reference from Power Automate using Managed Identity
```

> ⚠️ **Security rule:** Never store credentials as plain text in your flows. Always use environment variables, Key Vault, or connector authentication.

---

## 4.6 ⚠️ Error Handling — Don't Let Your Agent Break

Every external call can fail. Here's how to handle it gracefully.

### In Power Automate:

```
1. In every HTTP/connector action → Settings → "Configure run after"
2. Enable: "has failed" and "has timed out"
3. Add a parallel error branch:
   → Set variable: ErrorOccurred = true
   → Set variable: ErrorMessage = "Unable to reach ServiceNow"
4. Return to agent: 
   Success: true/false
   ErrorMessage: the reason if failed
```

### In Copilot Studio:

```
After calling the action, add a condition:

IF action.Success equals false:
  → Message: "I'm having trouble connecting to our ticketing system right now.
    
    🔄 Please try again in a few minutes, or:
    📧 Email directly: itsupport@contoso.com
    📞 Call: ext. 3000
    
    I've logged this issue for our team."
  → End conversation

IF action.Success equals true:
  → Continue with normal flow
```

---

## 4.7 📋 Lesson Summary

```
✅ What you built:
  IT Operations Agent with:
    ✅ Live employee lookup from SharePoint
    ✅ ServiceNow ticket creation via Power Automate
    ✅ Teams notification to IT channel
    ✅ Confirmation email to the employee
    ✅ Real-time system status from REST API
    ✅ Error handling for failed API calls

✅ What you learned:
  3 connection methods:
    1. Built-in connectors    → fastest, Microsoft 365 focused
    2. Power Automate flows   → most flexible, visual workflow
    3. Custom HTTP connector  → any REST API, full control

  Authentication patterns:
    API Key, Azure AD, OAuth2, Service Account

  Variables across boundaries:
    Passing inputs into flows
    Returning outputs back to agent

  Error handling:
    Power Automate failure branches
    Graceful agent fallback messages
```

---

## 🚀 Next Step

Your agent now talks AND acts. Time to make it **truly intelligent** — with generative AI, document knowledge bases, and MCP integration.

> 👉 **[Lesson 5 — Generative AI, Knowledge Bases & MCP →](05-generative-ai-knowledge.md)**

---

*[← Lesson 3: Topics & Variables](03-topics-variables.md) | [Back to Copilot Studio Guide](README.md)*
