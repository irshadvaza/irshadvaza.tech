📘 Chapter 02 – OneLake & Lakehouse Architecture

The Heart of Microsoft Fabric

🌊 1️⃣ What is OneLake?

OneLake is the central storage system of Microsoft Fabric.

It is:

The OneDrive for enterprise data.

Every workload inside Microsoft Fabric stores data in OneLake.

🧠 Why OneLake Was Created?

Before OneLake:

Each system had its own storage.

Data was copied multiple times.

Storage costs increased.

Governance became complex.

Microsoft solved this by introducing:

✅ One logical data lake for entire organization
✅ No duplication required
✅ Shared across all engines

🏗 2️⃣ Logical Structure of OneLake
Tenant
 └── OneLake
      ├── Workspace 1
      │     ├── Lakehouse
      │     ├── Warehouse
      │     └── Notebook
      ├── Workspace 2
      └── Workspace 3

Important Concept:

🔹 Each organization has one OneLake
🔹 Workspaces organize projects
🔹 Items (Lakehouse, Warehouse, etc.) store data inside it

🏢 3️⃣ What is a Lakehouse?

A Lakehouse combines:

Data Lake	Data Warehouse
Cheap storage	Structured analytics
Raw files	SQL tables
Big data	BI optimized

Fabric’s Lakehouse supports:

Files (CSV, Parquet, JSON)

Delta tables

Spark processing

SQL querying

🔥 4️⃣ Lakehouse Internal Structure

Inside a Lakehouse:

Lakehouse
 ├── Files
 └── Tables

📁 Files Section

Used for:

Raw ingestion

Staging data

External data

🗄 Tables Section

Used for:

Cleaned data

Structured Delta tables

Reporting datasets

🧪 5️⃣ Step-by-Step Practical Example (Retail Project)

Let’s build your first Lakehouse project.

🎯 Scenario

A retail company has:

sales.csv

customers.csv

products.csv

Goal:

Create analytics-ready tables.

🟢 Step 1 – Create Workspace

In Fabric portal:

New Workspace → Name: RetailAnalytics

🟢 Step 2 – Create Lakehouse

Inside workspace:

New → Lakehouse → Name: RetailLakehouse


Fabric automatically creates storage in OneLake.

🟢 Step 3 – Upload Raw Files

Go to:

Lakehouse → Files → Upload


Upload:

sales.csv

customers.csv

products.csv

Now stored in:

OneLake/RetailAnalytics/RetailLakehouse/Files/

🟢 Step 4 – Transform Using Notebook (Spark)

Create Notebook inside Lakehouse.

Example Code:
# Load sales data
df_sales = spark.read.csv("Files/sales.csv", header=True, inferSchema=True)

# Basic transformation
df_clean = df_sales.filter(df_sales["revenue"] > 0)

# Save as Delta table
df_clean.write.format("delta").saveAsTable("sales_clean")


What happened?

Read CSV

Cleaned data

Saved as Delta table

Stored in OneLake

Automatically appears in "Tables" section

🟢 Step 5 – Query Using SQL

Open SQL endpoint of Lakehouse.

SELECT region, SUM(revenue)
FROM sales_clean
GROUP BY region;


No data movement.
No duplication.

⚡ 6️⃣ What Makes This Powerful?

All engines read the same data:

Spark

SQL

Power BI

Data Science

Real-Time Analytics

Everything uses:

Delta format inside OneLake

🔄 7️⃣ Delta Lake Explained Simply

Fabric stores tables in:

Open Delta Lake format

Benefits:

Feature	Meaning
ACID	No partial updates
Time Travel	Query old versions
Schema Evolution	Add columns safely
Fast reads	Optimized storage

Example:

SELECT * FROM sales_clean VERSION AS OF 2;


You can query older versions.

🧬 8️⃣ Medallion Architecture in Fabric

Fabric supports:

Bronze → Silver → Gold pattern

🟤 Bronze (Raw)

Raw ingestion.

Example:

sales.csv

customers.csv

⚪ Silver (Cleaned)

Cleaned, validated data.

Example:

sales_clean

customers_clean

🟡 Gold (Business Ready)

Aggregated tables.

Example:

CREATE TABLE sales_summary AS
SELECT region, SUM(revenue) total_revenue
FROM sales_clean
GROUP BY region;

🎯 9️⃣ Direct Lake Mode (Revolutionary Feature)

With:

Power BI

Traditional approach:

Import data → Create model → Refresh needed.

Fabric approach:

Power BI reads directly from Delta table in OneLake.

No import.
No refresh.
Ultra-fast.

🔐 🔟 Security in OneLake

Uses:

Microsoft Entra ID

Supports:

Workspace-level access

Table-level permissions

Row-level security

Data masking

Example:

Restrict HR salary data to HR team only.

🏗 11️⃣ Physical Storage Behind the Scene

Internally:

Built on Azure Data Lake Gen2

Managed fully by Fabric

You never manage storage account manually

💰 12️⃣ Cost Efficiency Example

Without Fabric:

Separate storage

Separate Synapse pool

Separate Power BI capacity

With Fabric:

One storage

Shared compute

Unified capacity

Lower cost.

📊 13️⃣ End-to-End Flow Summary
Upload CSV
     ↓
Store in Files
     ↓
Spark Transform
     ↓
Save as Delta Table
     ↓
SQL Query
     ↓
Power BI Direct Lake Report


Single platform.
Single storage.
Single security.

🧠 14️⃣ Real Enterprise Use Case
Smart City Project

Data sources:

Traffic sensors

Weather API

Pollution monitoring

CCTV logs

Steps:

Data Factory ingests

Stored in Bronze

Cleaned in Silver

Aggregated in Gold

Power BI dashboard

AI prediction model runs on same data

All inside Fabric.

📌 15️⃣ Key Takeaways
Concept	Why Important
OneLake	Single source of truth
Lakehouse	Flexible analytics
Delta format	Reliable data
Medallion	Structured pipeline
Direct Lake	Real-time reporting
🎓 What You Learned in This Chapter

You now understand:

OneLake architecture

Lakehouse structure

Files vs Tables

Delta Lake

Medallion architecture

Direct Lake mode

Real-world implementation

You are now thinking like a Fabric Architect.
