# 🚀 Chapter 2: Creating Azure Data Factory (Step-by-Step Guide)

---

# 🎯 Objective of This Chapter

In this chapter, you will learn:

- How to create Azure Data Factory
- How to navigate ADF Studio
- How to understand the UI layout
- How to configure Git integration
- How to publish your first workspace

By the end of this chapter, you will have your own working Azure Data Factory.

---

# 🏗️ Step 1: Login to Azure Portal

1. Open browser
2. Go to: https://portal.azure.com
3. Login with your Azure account

You will land on the **Azure Portal Dashboard**.

---

# 🔎 Step 2: Search for Azure Data Factory

In the top search bar:

Type:

```
Data Factory
```

Click on:

**Data Factories**

Then click:

➕ **Create**

---

# ⚙️ Step 3: Configure Basic Settings

You will now see the "Create Data Factory" page.

Fill the following details:

## 🔹 Subscription
Select your Azure subscription.

## 🔹 Resource Group
Choose:
- Existing resource group  
OR  
- Create new (Recommended for learning)

Example:
```
rg-adf-learning
```

## 🔹 Name
Enter a globally unique name:

Example:
```
adf-learning-irshad
```

## 🔹 Region
Choose nearest region (Example: UAE North)

## 🔹 Version
Select:
```
V2 (Latest)
```

Click:
```
Review + Create
```

Then:
```
Create
```

Deployment takes 1–2 minutes.

---

# ✅ Step 4: Go to Resource

Once deployment completes:

Click:
```
Go to Resource
```

You will now see your Azure Data Factory Overview page.

---

# 🎨 Step 5: Open ADF Studio

Click:

```
Launch Studio
```

This opens the **Azure Data Factory Studio UI**

This is where you build pipelines.

---

# 🖥️ Understanding Azure Data Factory Studio (UI Walkthrough)

When Studio opens, you will see a clean UI with left-side navigation.

---

# 📂 ADF Studio Layout Overview

Left Panel Icons:

| Icon | Section | Purpose |
|------|---------|----------|
| 🏠 | Home | Quick start templates |
| ✏️ | Author | Create pipelines & datasets |
| 🔍 | Monitor | View pipeline runs |
| 🧰 | Manage | Linked services & IR |
| 📘 | Learn | Documentation |

---

# 🧭 Step 6: Explore Author Section

Click:

✏️ **Author**

Here you will create:

- Pipelines
- Datasets
- Dataflows

Right now, it is empty because we haven't created anything yet.

---

# 🧰 Step 7: Configure Linked Service (First Connection)

Before building pipelines, we must create a connection.

Click:

🧰 **Manage**

Then:

➕ **New Linked Service**

You will see 100+ connectors like:

- Azure SQL Database
- Blob Storage
- REST API
- SQL Server
- Databricks

For learning, select:

**Azure Blob Storage**

Click:
```
Continue
```

---

# 🔐 Configure Blob Storage Connection

Fill:

- Name: `ls_blob_storage`
- Authentication: Account Key
- Storage account name
- Test Connection

Click:
```
Create
```

🎉 Your first Linked Service is created.

---

# 🔄 What Just Happened?

You created a connection between:

Azure Data Factory → Storage Account

This connection will be used in pipelines.

---

# 🏗️ Step 8: Create First Pipeline (Empty Pipeline)

Go to:

✏️ **Author**

Click:

➕ → Pipeline → Pipeline

Rename it:

```
pl_first_pipeline
```

You now see a blank canvas.

This is your workflow design area.

---

# 🎯 Step 9: Add Copy Activity

From Activities panel (left side):

Drag:

```
Copy Data
```

Drop it onto canvas.

Click on the activity.

You will see 3 tabs:

- General
- Source
- Sink

---

# 📥 Configure Source

In Source tab:

Click:
```
+ New Dataset
```

Choose:
- Azure Blob Storage
- CSV file

Create dataset:
```
ds_source_csv
```

---

# 📤 Configure Sink

Go to Sink tab:

Click:
```
+ New Dataset
```

Choose:
- Azure Blob Storage
- CSV

Create:
```
ds_sink_csv
```

Now you have configured a simple copy activity.

---

# 🧪 Step 10: Debug the Pipeline

Click:
```
Debug
```

Pipeline will execute immediately.

Go to:
🔍 **Monitor**

You can see:

- Pipeline run status
- Activity run details
- Execution time
- Error logs (if any)

---

# 🚀 Step 11: Publish Changes

Important:

ADF works in two modes:

- Development Mode
- Published Mode

Click:
```
Publish All
```

This deploys your changes to live version.

---

# 🔁 Step 12: Add Trigger (Schedule)

To automate:

Click:
```
Add Trigger → New/Edit
```

Choose:
- Schedule Trigger

Set:
- Start Date
- Time
- Recurrence (Daily)

Click:
```
OK
```

Now pipeline runs automatically.

---

# 🌳 Optional: Configure Git Integration (Recommended)

Professional projects always use Git.

Go to:

🧰 Manage → Git Configuration

You can connect:

- Azure DevOps
- GitHub

Benefits:

- Version control
- Branching
- Collaboration
- CI/CD support

---

# 🔎 Monitor Section Explained

Go to:

🔍 Monitor

Here you can see:

- Pipeline runs
- Trigger runs
- Activity runs
- Failed runs
- Duration
- Error messages

This is your operational dashboard.

---

# 🧠 Beginner Analogy

Think of ADF Studio like:

- Author = Design room
- Manage = Connection room
- Monitor = Control room
- Publish = Deploy button

---

# 📌 Common Beginner Mistakes

❌ Forgetting to Publish  
❌ Not testing connection  
❌ Wrong region selection  
❌ Not using resource groups properly  
❌ Skipping Monitor checks  

---

# 🏁 What You Achieved in This Chapter

You successfully:

✔️ Created Azure Data Factory  
✔️ Launched ADF Studio  
✔️ Explored UI  
✔️ Created Linked Service  
✔️ Created First Pipeline  
✔️ Added Copy Activity  
✔️ Debugged Pipeline  
✔️ Published Changes  
✔️ Configured Trigger  

You are now officially working with Azure Data Factory 🎉

---

# 🚀 Coming Next in Chapter 3

In the next chapter, we will build:

👉 Real Copy Pipeline (SQL → Blob)  
👉 Parameterized Pipeline  
👉 Dynamic File Names  
👉 Error Handling Basics  

---

# 🎓 Final Summary

Creating Azure Data Factory involves:

1. Creating resource in Azure Portal
2. Launching Studio
3. Creating Linked Services
4. Designing Pipelines
5. Debugging
6. Publishing
7. Monitoring

You now have the foundation to start building real-world ETL pipelines.

---

✨ Congratulations! You have completed Chapter 2 – Creating Azure Data Factory.
