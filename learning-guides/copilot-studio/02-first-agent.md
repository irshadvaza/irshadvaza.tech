[Home](../../index.md) | [Learning Guides](../README.md) | [Copilot Studio](README.md) | [← Lesson 1](01-introduction.md) | [Lesson 3 →](03-topics-variables.md)

---

# 🏗️ Lesson 2 — Build Your First Agent in 30 Minutes

> **Stop reading. Start building. You'll have a live, working HR FAQ agent by the end of this lesson.**

**⏱ Time:** 60 minutes &nbsp;|&nbsp; **Level:** 🟢 Beginner &nbsp;|&nbsp; **Prerequisites:** Lesson 1 complete, Copilot Studio access

---

## 📋 What You'll Build

An **HR FAQ Agent** that employees can ask questions like:

- *"How many leave days do I get?"*
- *"What's the process for requesting equipment?"*
- *"Who do I contact for payroll issues?"*

By the end of this lesson, your agent will be live and testable — and you'll understand how to add any new topic in minutes.

---

## 📋 What You'll Learn

- [ ] Create a new agent from scratch
- [ ] Understand the agent canvas and topic editor
- [ ] Build 3 real conversation topics
- [ ] Use trigger phrases and branching responses
- [ ] Test your agent in the built-in emulator
- [ ] Publish to a shareable web channel

---

## 2.1 🚀 Create Your New Agent

### Step 1: Open Copilot Studio

Go to [https://web.powerva.microsoft.com](https://web.powerva.microsoft.com) and sign in.

### Step 2: Create the Agent

```
1. Click "+ Create" (top left) or "New agent" on the Home screen
2. Choose "New agent" (not a template — we're building from scratch)
3. Fill in the details:

   Name:         HR Assistant
   Description:  Helps employees with HR policies, leave, and payroll questions
   Instructions: You are a friendly HR assistant for Contoso Ltd. 
                 Always be professional, clear, and helpful. 
                 If you don't know the answer, direct the user to hr@contoso.com

4. Language: English (or your preferred language)
5. Click "Create"
```

> 💡 **The Instructions field is powerful.** This is your agent's system prompt — it sets the personality and ground rules for all generative AI responses.

---

## 2.2 🗺️ Exploring the Agent Canvas

When your agent opens, you'll see this layout:

```
┌──────────────────────────────────────────────────────────┐
│  HR Assistant                          [Test] [Publish]   │
├──────────┬───────────────────────────────────────────────┤
│ TOPICS   │                                               │
│          │         TOPIC CANVAS                          │
│ Overview │                                               │
│ ──────── │  ┌─────────────────────────────────────┐     │
│ System   │  │  Trigger Phrases                    │     │
│  topics  │  │  What the user might say            │     │
│          │  └────────────────┬────────────────────┘     │
│ ──────── │                   ↓                           │
│ Custom   │  ┌─────────────────────────────────────┐     │
│  topics  │  │  Message                            │     │
│ + Add    │  │  What the agent says back           │     │
│          │  └─────────────────────────────────────┘     │
└──────────┴───────────────────────────────────────────────┘
```

**System topics** are built-in — Greeting, Goodbye, Fallback (when the agent doesn't understand). **Custom topics** are the ones you build.

---

## 2.3 🔧 Understanding System Topics First

Before building your own, take 2 minutes to look at what's already there.

```
1. Click "Topics" in the left nav
2. Click the "System" tab
3. Click "Greeting" to open it
```

You'll see: a set of trigger phrases ("Hello", "Hi", "Hey") and a response message. This is the pattern for everything you'll build.

**Quick task:** Customize the Greeting to say:
```
Hello! I'm the Contoso HR Assistant 👋

I can help you with:
• Leave and time-off policies
• Equipment and IT requests  
• Payroll and benefits questions

What would you like to know?
```

Click **Save** after editing.

---

## 2.4 🏗️ Build Topic 1 — Annual Leave Policy

Now let's build your first custom topic.

### Step 1: Create the Topic

```
1. Click "Topics" → "+ Add topic" → "From blank"
2. Name your topic: "Annual Leave Policy"
```

### Step 2: Add Trigger Phrases

Trigger phrases are examples of what users might say. Add at least 5-8 for good accuracy:

```
Click "+ Add phrases" and enter each one:

• How many leave days do I get
• What is the annual leave policy
• How much annual leave do I have
• Leave entitlement
• How many days off per year
• What are my leave benefits
• Holiday allowance
• Days off policy
```

> 💡 **Best practice:** Don't add too many similar phrases. Instead, vary them — different lengths, different wordings. The AI handles synonyms naturally.

### Step 3: Add the Response

Click the **"+" button** below the trigger node → **"Send a message"**

Enter this message:

```markdown
📅 **Annual Leave Policy at Contoso**

Here's your leave entitlement based on your employment type:

| Employee Type | Annual Leave Days |
|---|---|
| Full-time (< 3 years) | 20 days |
| Full-time (3–5 years) | 25 days |
| Full-time (5+ years) | 30 days |
| Part-time | Pro-rata based on hours |

**Key rules:**
• Leave must be approved by your line manager
• Requests should be submitted at least 2 weeks in advance
• Maximum 10 days can be carried over to next year

Would you like to know how to **submit a leave request**?
```

### Step 4: Add a Branch (Yes/No Follow-up)

Below the message node, click **"+"** → **"Ask a question"**:

```
Question: Would you like to know how to submit a leave request?
Options: 
  [Yes, show me how]
  [No, that's all I need]
```

For the **"Yes"** branch, add another message:

```
📝 **How to Submit a Leave Request**

1. Log into the HR Portal at hr.contoso.com
2. Click "My Leave" → "New Request"
3. Select dates and leave type
4. Add a note for your manager (optional)
5. Click "Submit" — your manager will be notified automatically

You'll receive an email confirmation within 24 hours. ✅
```

For the **"No"** branch, add:

```
No problem! Is there anything else I can help you with? 😊
```

### Step 5: Save

Click **Save** (top right). Your first topic is done.

---

## 2.5 🏗️ Build Topic 2 — IT Equipment Request

```
1. Click "+ Add topic" → "From blank"
2. Name: "Equipment Request"
```

**Trigger phrases:**
```
• I need a new laptop
• Request equipment
• How do I get a new monitor
• Equipment request process
• New hire laptop
• Order IT equipment
• I need hardware
```

**Conversation flow — this time with a question to collect info:**

Add a **"Send a message"** node:
```
Great! I can help you request equipment. Let me collect a few details.
```

Then add **"Ask a question"** node:
```
Question: What type of equipment do you need?
Options:
  [💻 Laptop]
  [🖥️ Monitor / Desktop]  
  [🖱️ Peripherals (mouse, keyboard)]
  [📱 Mobile Device]
  [Other]
```

Save the answer to a variable: `Topic.EquipmentType`

Add another **"Ask a question"**:
```
Question: Is this for yourself or a new team member?
Options:
  [For me]
  [For a new hire]
```

Save to: `Topic.RequestFor`

Then add a final message:
```
✅ Got it! Here's a summary of your request:

Equipment: {Topic.EquipmentType}
Requested for: {Topic.RequestFor}

**Next steps:**
1. Submit a formal request at: it.contoso.com/requests
2. Approval takes 1–3 business days
3. Your IT team will contact you to arrange delivery

💡 **Pro tip:** New hire requests should be submitted at least 5 working days before the start date.

Need anything else? 😊
```

**Save** the topic.

---

## 2.6 🏗️ Build Topic 3 — Payroll & Benefits

```
Name: "Payroll and Benefits"
```

**Trigger phrases:**
```
• Payroll question
• When do I get paid
• Pay date
• Salary payment
• Benefits and perks
• What benefits do I get
• Health insurance
• Pension contribution
• Pay slip
```

**Response:**

```
💰 **Payroll & Benefits at Contoso**

**Pay Schedule:**
📅 Salaries are paid on the **last working day** of each month
📧 Your payslip is emailed to your registered email address

**Benefits Summary:**
| Benefit | Details |
|---|---|
| 🏥 Health Insurance | 100% covered for employee, 50% for family |
| 🦷 Dental & Vision | Included in health plan |
| 🏖️ Annual Leave | See leave policy |
| 👶 Parental Leave | 16 weeks full pay |
| 💼 Pension | Company contributes 6% |
| 🏋️ Gym | £50/month reimbursement |
| 📚 Learning | £1,000 annual training budget |

**For specific payroll queries:**
📧 Email: payroll@contoso.com
📞 Call: ext. 2200 (Mon–Fri, 9am–5pm)

Is there anything else I can help you with?
```

**Save.**

---

## 2.7 🧪 Test Your Agent

Now let's see it in action.

```
1. Click "Test" button (top right) — a chat panel opens
2. Try these test messages:

   → "Hi"                              (should trigger Greeting)
   → "How many leave days do I get?"   (should trigger Annual Leave)
   → "Yes, show me how"                (should show submission steps)
   → "I need a laptop"                 (should trigger Equipment)
   → "When do I get paid?"             (should trigger Payroll)
   → "What's the weather?"             (should trigger Fallback)
```

**What to check:**
- ✅ Does the right topic trigger?
- ✅ Are the messages clear and readable?
- ✅ Do the branches work correctly?
- ✅ Does the fallback handle unknown questions gracefully?

> 💡 **When a wrong topic triggers:** Go back to that topic and add or adjust the trigger phrases. The AI learns from more examples.

---

## 2.8 📊 View the Conversation Map

While testing, you can see which topic was triggered:

```
In the Test panel:
→ Each message shows which Topic was activated
→ You can click "Track" to follow the conversation through the canvas
→ Variable values appear in the Variables panel on the right
```

This is essential for debugging.

---

## 2.9 🌐 Publish Your Agent

Your agent currently only works in the test environment. Let's publish it.

### Step 1: Publish

```
1. Click "Publish" (top right corner)
2. Review the summary — confirm you want to publish
3. Click "Publish" to confirm
4. Wait 1–2 minutes for the publishing process
```

### Step 2: Share via Demo Website

```
1. After publishing, go to "Settings" → "Channels"
2. Click "Demo website" 
3. Copy the URL — share this with anyone to test your agent
4. It works in any browser, no login required
```

> 🎉 **You now have a live AI agent with a public URL.**

---

## 2.10 📋 Lesson Summary

```
✅ What you built:

  Agent: HR Assistant (Contoso Ltd)
  Topics created:
    1. Annual Leave Policy     → with branching follow-up
    2. Equipment Request       → with variable collection
    3. Payroll & Benefits      → with structured table response
  
  Tested:  ✅ In built-in emulator
  Live at: ✅ Demo website URL

✅ What you learned:

  Agent creation      → name, description, instructions
  Topic structure     → trigger phrases + conversation nodes
  Message types       → plain text, markdown, tables
  Ask a question      → collecting user input with options
  Variables           → storing answers for later use
  Branching           → different paths based on user choice
  Publishing          → making the agent live
  Channels            → Demo website as a quick share link
```

---

## 🚀 Challenge (Optional)

Before moving on, try adding one more topic:

> **Topic: "Sick Leave"** — What's the policy, how to notify your manager, and what documentation is needed.

This will cement the pattern in your memory.

---

## 🚀 Next Step

Your agent works. Now let's make it **intelligent** — handling complex conversations, understanding context, and remembering what the user said.

> 👉 **[Lesson 3 — Conversations, Topics & Variables →](03-topics-variables.md)**

---

*[← Lesson 1: Introduction](01-introduction.md) | [Back to Copilot Studio Guide](README.md)*
