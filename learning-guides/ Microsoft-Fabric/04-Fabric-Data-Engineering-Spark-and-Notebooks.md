📘 Chapter 04 – Fabric Data Engineering (Spark & Notebooks Deep Dive)

From Beginner to Enterprise Data Engineer

🚀 1️⃣ Introduction to Fabric Data Engineering

Inside Microsoft Fabric, Data Engineering is powered by:

Apache Spark (fully managed, SaaS, auto-scaled)

You do NOT:

Manage clusters

Configure infrastructure

Handle scaling manually

Fabric manages compute automatically.

🧠 2️⃣ What is Apache Spark (Simple Explanation)?

Apache Spark is a distributed engine that:

Processes large datasets

Runs parallel operations

Supports Python, SQL, Scala

Imagine:

Instead of 1 computer processing 1 million rows,
Spark uses multiple executors in parallel.

1M rows
 ↓
Split into chunks
 ↓
Processed simultaneously
 ↓
Results combined


Fabric runs Spark behind the scenes.

🏗 3️⃣ Spark Architecture in Fabric
User Notebook
     ↓
Spark Driver
     ↓
Executors (Parallel Workers)
     ↓
OneLake (Storage)


Storage layer is:

OneLake

Everything reads and writes to Delta tables in OneLake.

🧪 4️⃣ Your First Fabric Notebook (Step-by-Step)
🎯 Scenario: Retail Analytics Project

We have:

sales.csv (1M rows)

customers.csv

products.csv

Goal:

Create analytics-ready Gold table.

🟢 Step 1 – Create Notebook

Inside Lakehouse:

New → Notebook → Name: Retail_Data_Engineering


Select language: Python

🟢 Step 2 – Load Raw Data (Bronze Layer)
df_sales = spark.read.csv("Files/sales.csv", header=True, inferSchema=True)

df_sales.display()


Now Spark loads file from OneLake.

🟢 Step 3 – Basic Transformations

Remove invalid revenue:

df_clean = df_sales.filter(df_sales["revenue"] > 0)


Add calculated column:

from pyspark.sql.functions import col

df_clean = df_clean.withColumn("profit", col("revenue") - col("cost"))

🟢 Step 4 – Save as Delta Table (Silver Layer)
df_clean.write.format("delta").mode("overwrite").saveAsTable("sales_clean")


Now visible in:

Lakehouse → Tables → sales_clean

Stored as Delta in OneLake.

🟢 Step 5 – Create Gold Layer Aggregation
from pyspark.sql.functions import sum

df_gold = df_clean.groupBy("region") \
                  .agg(sum("revenue").alias("total_revenue"),
                       sum("profit").alias("total_profit"))

df_gold.write.format("delta").mode("overwrite").saveAsTable("sales_summary")


Now ready for Power BI.

⚡ 5️⃣ Understanding Delta Lake in Fabric

Fabric stores tables in:

Open Delta Lake format

Benefits:

Feature	Why Important
ACID Transactions	No partial writes
Time Travel	Query older versions
Schema Evolution	Add columns safely
Fast reads	Optimized Parquet

Example:

SELECT * FROM sales_clean VERSION AS OF 1;

🔄 6️⃣ Partitioning Strategy (Performance Tuning)

If table has millions of rows:

Partition by:

Date

Region

Category

Example:

df_clean.write.format("delta") \
    .partitionBy("region") \
    .mode("overwrite") \
    .saveAsTable("sales_partitioned")


Why?

Instead of scanning full table,
Spark scans only required partition.

Huge performance boost.

🧬 7️⃣ Medallion Architecture with Spark
Bronze  → Raw data
Silver  → Cleaned & validated
Gold    → Aggregated business layer


Example mapping:

Layer	Table
Bronze	sales_raw
Silver	sales_clean
Gold	sales_summary
📊 8️⃣ Working with Large Dataset (1M+ Rows Example)

Simulate 1M rows:

from pyspark.sql.functions import rand

df_big = spark.range(0, 1000000) \
    .withColumn("revenue", rand()*1000) \
    .withColumn("cost", rand()*500)

df_big.write.format("delta").saveAsTable("big_sales")


Spark processes this in seconds.

Traditional SQL server may struggle.

🔍 9️⃣ Spark SQL in Fabric

You can use SQL inside notebook:

%%sql

SELECT region, SUM(revenue)
FROM sales_clean
GROUP BY region;


Spark + SQL flexibility.

🚀 🔟 Caching for Performance

If dataset reused multiple times:

df_clean.cache()


Why?

Keeps data in memory

Avoids recomputation

Faster execution

🧪 11️⃣ Handling Null Values
df_clean = df_clean.fillna(0)


Or specific column:

df_clean = df_clean.fillna({"revenue":0})

🔁 12️⃣ Incremental Load Strategy

Instead of full reload:

df_new = spark.read.csv("Files/new_sales.csv", header=True)

df_new.write.format("delta") \
    .mode("append") \
    .saveAsTable("sales_clean")


Efficient for enterprise pipelines.

🧠 13️⃣ Real Enterprise Use Case
Smart City Traffic Monitoring

Data:

5M sensor records daily

Vehicle speed

Location

Timestamp

Pipeline:

Ingest raw sensor data (Bronze)

Remove corrupted records (Silver)

Aggregate hourly congestion stats (Gold)

Power BI real-time dashboard

ML prediction model

All inside Fabric.

🔐 14️⃣ Security in Spark Layer

Uses:

Microsoft Entra ID

Supports:

Table-level security

Row-level security

Workspace roles

Example:

Only Finance role can query profit columns.

🏎 15️⃣ Optimization Techniques
Technique	Benefit
Partitioning	Faster filtering
Caching	Reuse data
Z-Ordering	Faster selective queries
Incremental loads	Lower cost
Proper schema	Avoid inferSchema overhead
🎯 16️⃣ Spark vs Traditional SQL Server
SQL Server	Spark
Single machine	Distributed
Limited scale	Massive scale
Expensive scaling	Elastic
Structured only	Structured + Semi-structured
📊 17️⃣ End-to-End Engineering Flow
Raw CSV
   ↓
Spark Load
   ↓
Clean & Transform
   ↓
Save Delta Table
   ↓
Aggregate
   ↓
Power BI Direct Lake


Direct integration with:

Power BI

No data duplication required.

🧑‍💼 18️⃣ Interview-Level Understanding

If asked:

❓ What is Fabric Data Engineering?

Answer:

Fabric Data Engineering is a fully managed Spark-based big data processing environment integrated with OneLake, enabling scalable transformation, optimization, and Delta Lake management within Microsoft Fabric.

🏆 19️⃣ Why Fabric Spark is Powerful?

No cluster management

Unified storage

Native Delta

Direct BI integration

Enterprise security

SaaS simplicity

📌 20️⃣ Key Takeaways

You now understand:

Spark basics

Notebook creation

Delta Lake

Partitioning

Performance tuning

Incremental loads

Enterprise architecture

You are now thinking like:

🎓 Fabric Data Engineer & Architect

📚 Next Chapter
