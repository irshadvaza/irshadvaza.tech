# 🚀 Chapter 4: Metadata-Driven & Parameterized Pipeline (Enterprise Design)

---

# 🎯 Objective of This Chapter

In this chapter, you will learn:

- What is Metadata-Driven Design
- Why enterprises use parameterized pipelines
- How to use Pipeline Parameters
- How to use Dynamic Content
- How to use Get Metadata Activity
- How to retrieve:
  - Exists
  - Item Count
  - Child Items
  - Last Modified
- How to build one pipeline for multiple files

By the end of this chapter, you will move from beginner to **enterprise-level ADF design**.

---

# 🧠 What is Metadata-Driven Pipeline?

Instead of creating:

❌ 10 pipelines for 10 tables  
❌ 20 pipelines for 20 files  

We create:

✅ 1 Generic Pipeline  
✅ Controlled by Parameters  
✅ Driven by Metadata  

This is how large enterprises design scalable systems.

---

# 🏢 Real Enterprise Scenario

Imagine you have Data Lake folder:

```
raw/input/
    product.csv
    customer.csv
    sales.csv
    inventory.csv
```

Instead of hardcoding file names…

We design a dynamic pipeline that:

- Checks if file exists
- Gets file count
- Reads metadata
- Processes dynamically

---

# 📌 Step 1: Create Parameterized Pipeline

Go to:

Author → + → Pipeline

Rename:

```
pl_metadata_driven_ingestion
```

---

# ⚙️ Step 2: Create Pipeline Parameters

Click on blank canvas → Parameters tab

Create parameters:

| Name | Type | Default Value |
|------|------|---------------|
| p_folder_path | String | raw/input |
| p_file_name | String | product.csv |

Now this pipeline can accept different file names dynamically.

---

# 📂 Step 3: Create Dataset with Parameters

Create new Dataset:

Azure Data Lake Storage Gen2 → Delimited Text

In dataset settings:

Create parameters:

| Name | Type |
|------|------|
| folderPath | String |
| fileName | String |

In Connection tab:

Folder path:
```
@dataset().folderPath
```

File name:
```
@dataset().fileName
```

Name dataset:

```
ds_adls_dynamic_file
```

Now dataset is dynamic.

---

# 🔄 Step 4: Pass Pipeline Parameters to Dataset

Inside pipeline:

Add Copy Activity (optional for later).

For dataset configuration:

Folder Path:
```
@pipeline().parameters.p_folder_path
```

File Name:
```
@pipeline().parameters.p_file_name
```

Now pipeline controls dataset.

---

# 🔎 Step 5: Add Get Metadata Activity (Important)

From Activities panel:

Drag:

```
Get Metadata
```

Rename:

```
get_file_metadata
```

Connect it with dataset:

`ds_adls_dynamic_file`

---

# 📋 Step 6: Configure Get Metadata Fields

Click on Get Metadata activity.

In Field List, select:

✔️ Exists  
✔️ Item Name  
✔️ Item Type  
✔️ Size  
✔️ Last Modified  
✔️ Child Items  
✔️ Item Count  

Now this activity will retrieve metadata details.

---

# 🧪 Practical Scenario 1: Check If File Exists

After Get Metadata:

Add **If Condition Activity**

Expression:

```
@activity('get_file_metadata').output.exists
```

If TRUE:
- Continue processing

If FALSE:
- Send alert
- Fail pipeline
- Log message

This prevents pipeline failure due to missing file.

---

# 📊 Practical Scenario 2: Get Item Count

If dataset points to folder:

Example:
```
raw/input/
```

Then select:

✔️ Child Items  
✔️ Item Count  

Output will show:

```
"itemCount": 4
```

Use expression:

```
@activity('get_file_metadata').output.itemCount
```

This helps in dynamic looping.

---

# 🔁 Step 7: Process Multiple Files Using ForEach

After Get Metadata:

Add:

```
ForEach Activity
```

Items:

```
@activity('get_file_metadata').output.childItems
```

Inside ForEach:

Add Copy Activity.

For dynamic file name:

```
@item().name
```

Now pipeline will loop through all files automatically.

---

# 🧪 Practical Scenario 3: Your product.csv Testing

You mentioned you:

- Dragged Get Metadata
- Connected dataset
- Set folder input
- File name: product.csv
- Tested fields like:
  - Exists
  - Child Items
  - Count

Here’s what happens internally:

If you specify:

Folder: raw/input  
File: product.csv  

And select:

✔️ Exists  

Output:
```
{
  "exists": true
}
```

If you select:

✔️ Size  

Output:
```
{
  "size": 2458
}
```

If you select:

✔️ Last Modified  

Output:
```
{
  "lastModified": "2026-02-22T08:45:12Z"
}
```

If dataset is folder only and you select:

✔️ Child Items  

Output:
```
{
  "childItems": [
    {"name": "product.csv"},
    {"name": "customer.csv"},
    {"name": "sales.csv"}
  ]
}
```

This is powerful for automation.

---

# 🔥 Step 8: Full Enterprise Metadata Flow

```
Get Metadata (Check Folder)
        ↓
If Condition (Exists?)
        ↓
ForEach (Loop Files)
        ↓
Copy Activity
        ↓
Store in Processed Layer
```

Single pipeline handles unlimited files.

---

# 📈 Advanced Enterprise Pattern: Table-Driven Metadata

Instead of hardcoding parameters…

Create control table in SQL:

```
TableName | SourceFolder | FileName | IsActive
------------------------------------------------
product   | raw/input    | product.csv | 1
customer  | raw/input    | customer.csv | 1
```

Pipeline reads control table → processes dynamically.

This is called:

**Metadata-Driven Architecture**

---

# 🧠 Why Enterprises Love This Design

✔️ Scalable  
✔️ Maintainable  
✔️ No duplicate pipelines  
✔️ Centralized configuration  
✔️ Easy onboarding for new tables  
✔️ Reduced cost  

---

# 🧪 Debugging Metadata Activity

Click:
```
Debug
```

Go to:
Monitor → Activity Output

Check:

- exists
- size
- itemCount
- childItems

Always validate output JSON before using expressions.

---

# ❌ Common Mistakes

❌ Forgetting to parameterize dataset  
❌ Using wrong dynamic expression  
❌ Not checking exists before processing  
❌ Hardcoding file names  
❌ Not handling empty folders  

---

# 🏗️ Enterprise Folder Structure Example

```
datalake/
    raw/
    processed/
    curated/
```

Pipeline should:

- Ingest to raw
- Transform to processed
- Publish to curated

---

# 🏁 What You Achieved

You built:

✔️ Parameterized Pipeline  
✔️ Dynamic Dataset  
✔️ Get Metadata Implementation  
✔️ Exists Check  
✔️ Item Count Retrieval  
✔️ Child Item Looping  
✔️ Enterprise-Ready Architecture  

This is how large-scale ADF systems are designed.

---

# 🚀 Coming Next in Chapter 5

Next chapter:

- Watermark Incremental Load
- Last Modified Based Load
- Delta Load Strategy
- Handling Updates
- Production Error Handling

You are now moving toward **ADF Solution Architect Level**.

---

# 🎓 Final Summary

Metadata-driven pipeline design allows you to:

- Control pipelines dynamically
- Reduce duplication
- Scale ingestion
- Automate file discovery
- Handle enterprise complexity

Instead of building multiple pipelines…

You build one intelligent pipeline.

---

✨ Congratulations! You have completed Chapter 4 – Metadata-Driven & Parameterized Pipeline.
