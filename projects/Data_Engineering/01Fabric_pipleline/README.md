# 🌍 World Population Analytics — End-to-End Azure Data Engineering Project

> **Built with:** Microsoft Fabric · PySpark · Delta Lake · Power BI · Medallion Architecture

---

## 📌 Project Overview

This is my first **end-to-end data engineering project** built entirely on **Microsoft Fabric** (Azure's unified analytics platform). The goal is to take raw, messy world population data — spread across three files on GitHub — clean it up layer by layer, and turn it into a beautiful, live Power BI dashboard that updates automatically every time the pipeline runs.

Think of this like a **data factory assembly line**:
- 🥉 **Bronze** → Raw data, exactly as it came from the source
- 🥈 **Silver** → Cleaned, validated, and structured data
- 🥇 **Gold** → Business-ready data, aggregated and ready for reporting

This pattern is called the **Medallion Architecture** — one of the most widely used patterns in modern data engineering.

---

## 🗂️ Dataset

Three CSV files hosted on GitHub, containing world population statistics by country, age group, and year:

| File | Description |
|------|-------------|
| `WPP2022_PopulationByAge5GroupSex_Medium_1.csv` | Population data (Part 1) |
| `WPP2022_PopulationByAge5GroupSex_Medium_2.csv` | Population data (Part 2) |
| `WPP2022_PopulationByAge5GroupSex_Medium_3.csv` | Population data (Part 3) |
| `metadata.json` | Metadata file containing all three file names |

**Source:** [GitHub Dataset Folder](https://github.com/irshadvaza/irshadvaza.tech/tree/main/Dataset)

**Key fields used:**
- `Location` — Country or region name
- `Time` — Year of the record
- `AgeGrp` — Age group (e.g., `5-9`, `10-14`)
- `PopMale` — Male population count
- `PopFemale` — Female population count

---

## 🏗️ Architecture Diagram

```
GitHub (3 CSV files)
        │
        ▼
┌─────────────────────┐
│   Data Factory      │  ← Lookup → For Each → Copy Activity
│   Pipeline          │  ← Failure Alert via Outlook Email
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Bronze Lakehouse  │  ← Raw data stored as Delta table
│   (Bronze_LH)       │    Table: tbl_Bronze_Fact
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Notebook          │  ← PySpark data cleaning
│   (Data Wrangling)  │    Fix AgeGrp values, rename columns,
│                     │    cast data types, unpivot Gender
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Silver Lakehouse  │  ← Clean, structured Delta table
│   (Silver_LH)       │    Table: silver_Fact4
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Gold Layer        │  ← Aggregated, business-ready data
│                     │    Optimised for reporting
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Semantic Layer     │  ← Power BI Dataset (auto-refresh)
│  + Power BI         │    Live Dashboard
└─────────────────────┘
```

---

## 🚀 Step-by-Step Walkthrough

---

### Step 1 — Create a Microsoft Fabric Workspace

A **Workspace** in Microsoft Fabric is like a project folder where all your resources live — lakehouses, pipelines, notebooks, and reports.

**How to create it:**
1. Go to [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
2. Click **Workspaces** in the left sidebar
3. Click **+ New workspace**
4. Give it a name like `WorldPopulation_Project`
5. Click **Apply**

> 💡 **Why?** Every object you create (Bronze Lakehouse, Silver Lakehouse, Notebooks, Pipelines) lives inside this workspace. It keeps everything organised in one place.

---

### Step 2 — Create the Bronze Lakehouse

A **Lakehouse** is like a database but built on top of cloud storage. It stores data as files (Parquet/Delta format) and lets you query them like tables using SQL or PySpark.

**How to create it:**
1. Inside your workspace, click **+ New item**
2. Search for **Lakehouse** and select it
3. Name it `Bronze_LH`
4. Click **Create**

> 💡 **Why Bronze?** In the Medallion Architecture, Bronze is the **landing zone** — you drop data here exactly as it arrives from the source. No cleaning, no transformation. This is important because if something goes wrong downstream, you can always come back and reprocess from Bronze.

---

### Step 3 — Build the Data Pipeline (Ingest All 3 Files)

This is the **most important step** — building a pipeline that automatically reads the metadata file (which lists all three dataset filenames), loops through each one, and copies it into the Bronze Lakehouse.

#### 3.1 — Create the Pipeline

1. In your workspace, click **+ New item** → **Data pipeline**
2. Name it `Pipeline_IngestPopulationData`

#### 3.2 — Add a Lookup Activity

The **Lookup** activity reads the `metadata.json` file from GitHub. This file contains the list of all three CSV filenames. Instead of hardcoding filenames in the pipeline, we read them dynamically — so if you add a new file to the metadata, the pipeline picks it up automatically.

**Configure Lookup:**
- **Source:** HTTP connection to your GitHub raw file URL
- **URL format:**
  ```
  https://raw.githubusercontent.com/irshadvaza/irshadvaza.tech/main/Dataset/metadata.json
  ```
- **Connection type:** HTTP (anonymous)
- **First row only:** ❌ Disabled (we want ALL file names)

> 💡 **Why Lookup?** Instead of copying each file manually with three separate activities, the Lookup reads the file list dynamically. This makes the pipeline scalable — if you add a 4th or 5th file tomorrow, you don't touch the pipeline.

#### 3.3 — Add a ForEach Activity

Connect the **Lookup** output to a **ForEach** activity. This loops through each filename returned by the Lookup.

**Configure ForEach:**
- **Items:** `@activity('Lookup1').output.value`
- **Sequential:** ✅ (processes one file at a time — safer for beginners)

#### 3.4 — Add a Copy Activity (Inside ForEach)

Inside the ForEach, add a **Copy Data** activity. This is what actually downloads each CSV and saves it to the Bronze Lakehouse.

**Source settings:**
- **Connection type:** HTTP
- **Base URL:**
  ```
  https://raw.githubusercontent.com/irshadvaza/irshadvaza.tech/main/Dataset/
  ```
- **Relative URL (dynamic):** `@{item().FileName}` ← this picks up each filename from the loop
- **File format:** DelimitedText (CSV)

**Destination settings:**
- **Connection:** Your `Bronze_LH` Lakehouse
- **Table name:** `tbl_Bronze_Fact`
- **Write behaviour:** Append (so all 3 files land in one table)

> 💡 **Why one table?** All three CSVs have the same schema (same columns), so we append them into a single table called `tbl_Bronze_Fact`. This makes downstream processing much simpler.

#### 3.5 — Add a Failure Alert (Email Notification)

No pipeline is perfect — data sources go down, files change format, connections timeout. You want to know when something breaks.

**How to add:**
1. Click the **Copy Activity** → go to the **On failure** path (the red arrow)
2. Add an **Office 365 Outlook** activity
3. Connect your Outlook account
4. Set **To:** your email address
5. **Subject:** `⚠️ Pipeline Failed — WorldPopulation Ingestion`
6. **Body:**
   ```
   The data ingestion pipeline has failed.
   Activity: @{activity('Copy_BronzeLoad').error.message}
   Time: @{utcNow()}
   Please investigate immediately.
   ```

> 💡 **Why this matters?** In real production environments, data pipelines run on schedules (e.g., nightly at 2 AM). You won't be watching a screen — the email alert wakes you up before anyone notices the dashboard is stale.

---

### Step 4 — Create a Notebook and Clean the Data (Bronze → Silver)

Raw data is almost never clean. Our population files had several data quality issues that needed fixing before the data could be trusted.

#### 4.1 — Create a New Notebook

1. In your workspace, click **+ New item** → **Notebook**
2. Name it `Notebook_BronzeToSilver`
3. Attach it to your `Bronze_LH` Lakehouse

#### 4.2 — Load Data from Bronze

```python
# Read the raw data from Bronze Lakehouse
df = spark.sql("SELECT * FROM Bronze_LH.tbl_Bronze_Fact")
display(df)
```

#### 4.3 — Select Only the Columns We Need

The raw files have many columns — we only care about 5 of them.

```python
df = df.select(["Location", "Time", "AgeGrp", "PopMale", "PopFemale"])
```

> 💡 **Why select fewer columns?** Keeping only what you need reduces storage costs, speeds up queries, and makes the data easier to understand for anyone who picks it up later.

#### 4.4 — Explore Data Quality Issues

Before fixing anything, we need to *find* the problems. We group by each column and count distinct values to spot anomalies.

```python
from pyspark.sql import functions as F

# Check all unique AgeGrp values — this is where we spotted the problems
display(df.groupBy('AgeGrp').agg({"AgeGrp": "count"}))
```

**What we found:**

| Dirty Value | What It Should Be | Root Cause |
|-------------|-------------------|------------|
| `09-May` | `5-9` | Excel auto-converted `5-9` to a date (May 9th) |
| `9-May` | `5-9` | Same Excel issue, slightly different format |
| `14-Oct` | `10-14` | Excel auto-converted `10-14` to a date (Oct 14th) |
| `#N/A` | `NA` | Excel error values exported as text |

> 💡 **This is a very common real-world problem!** When someone opens a CSV in Excel and saves it, Excel silently converts values like `5-9` into dates. It then exports them back as `09-May` instead of `5-9`. This is one of the most notorious data quality bugs in enterprise data engineering.

```python
# Verify the other columns too
display(df.groupBy('Location').agg({"Location": "count"}))
display(df.groupBy('Time').agg({"Time": "count"}))
```

#### 4.5 — Fix the AgeGrp Column

```python
# Fix the Excel date corruption
df = df.withColumn('AgeGrp', F.regexp_replace('AgeGrp', "09-May ", "5-9"))
df = df.withColumn('AgeGrp', F.regexp_replace('AgeGrp', "9-May", "5-9"))
df = df.withColumn('AgeGrp', F.regexp_replace('AgeGrp', "14-Oct", "10-14"))

# Fix the #N/A error values
df = df.withColumn('AgeGrp', F.regexp_replace('AgeGrp', "#N/A", "NA"))
```

> 💡 **What is `regexp_replace`?** It's like "Find & Replace" in Word, but for an entire column of millions of rows. `F.regexp_replace('column_name', 'find_this', 'replace_with_this')`.

#### 4.6 — Rename Columns and Fix Data Types (Generated by Data Wrangler)

Microsoft Fabric's **Data Wrangler** is a visual tool (like a spreadsheet editor) that lets you make transformations by clicking buttons — and then generates the PySpark code for you automatically. This is the code it generated:

```python
from pyspark.sql import types as T

def clean_data(df):
    # Rename columns to friendlier names
    df = df.withColumnRenamed('PopMale', 'Male')
    df = df.withColumnRenamed('PopFemale', 'Female')

    # Fix data types — Time should be a number, not text
    df = df.withColumn('Time', df['Time'].cast(T.LongType()))

    # Population figures should be decimals (some countries have fractional projections)
    df = df.withColumn('Male', df['Male'].cast(T.DoubleType()))
    df = df.withColumn('Female', df['Female'].cast(T.DoubleType()))

    return df

df_clean = clean_data(df)
display(df_clean)
```

> 💡 **Data Wrangler tip:** You can launch Data Wrangler from the toolbar in any Fabric Notebook. It gives you a visual preview of your data and generates production-ready PySpark code. Great for beginners!

#### 4.7 — Unpivot the Gender Columns

Right now, Male and Female are two separate columns. For Power BI dashboards, it's much easier to work with data in a **long format** — one row per person-group, with a `Gender` column and a `Population` column.

**Before unpivot:**
| Location | Time | AgeGrp | Male | Female |
|----------|------|--------|------|--------|
| India | 2020 | 5-9 | 45000 | 43000 |

**After unpivot:**
| Location | Time | AgeGrp | Gender | Population |
|----------|------|--------|--------|------------|
| India | 2020 | 5-9 | Male | 45000 |
| India | 2020 | 5-9 | Female | 43000 |

```python
df_clean = df_clean.unpivot(
    ['Location', 'Time', 'AgeGrp'],  # columns to keep
    ['Male', 'Female'],               # columns to unpivot
    'Gender',                         # new column name for Male/Female
    'Population'                      # new column name for the values
)
```

> 💡 **Why unpivot?** Power BI slicers and filters work much better when Gender is a single column. You can now filter by "Male" or "Female" with one click. This structure is called **tidy data** — one observation per row.

#### 4.8 — Save to Silver Lakehouse

```python
df_clean.write.format("delta").saveAsTable("silver_Fact4")
```

> 💡 **Delta format** stores your data with version history, ACID transactions, and lightning-fast queries. It's the storage backbone of Microsoft Fabric.

---

### Step 5 — Create the Gold Layer

The **Gold Layer** is your business-ready, aggregated data. It's optimised for the specific questions your dashboard will answer.

Create a new notebook `Notebook_SilverToGold` and create aggregated views or tables:

```python
# Read from Silver
df_silver = spark.sql("SELECT * FROM silver_Fact4")

# Example Gold aggregation — Total population by country and year
df_gold_country = df_silver.groupBy("Location", "Time") \
    .agg(F.sum("Population").alias("TotalPopulation"))

# Save to Gold
df_gold_country.write.format("delta").mode("overwrite").saveAsTable("gold_PopByCountry")

# Another Gold table — Population by Age Group
df_gold_age = df_silver.groupBy("AgeGrp", "Time") \
    .agg(F.sum("Population").alias("TotalPopulation"))

df_gold_age.write.format("delta").mode("overwrite").saveAsTable("gold_PopByAge")
```

> 💡 **Why a separate Gold layer?** The Silver layer has every single row of data — potentially hundreds of millions of records. The Gold layer pre-aggregates only what Power BI needs, making your dashboards blazing fast. Gold tables are optimised for humans (analysts, managers), not machines.

---

### Step 6 — Create the Semantic Layer in Power BI

This is where the magic happens. The **Semantic Layer** (also called a Power BI Dataset or Semantic Model) sits between your Gold data and your dashboard.

**How to create it:**
1. In your workspace, click **+ New item** → **Semantic model**
2. Connect it to your Gold Lakehouse tables (`gold_PopByCountry`, `gold_PopByAge`)
3. Define relationships between tables
4. Create calculated measures:
   ```dax
   Total Population = SUM(gold_PopByCountry[TotalPopulation])
   
   Male Population = CALCULATE(SUM(gold_PopByCountry[TotalPopulation]), gender_filter = "Male")
   
   YoY Growth % = 
   DIVIDE(
       [Total Population] - CALCULATE([Total Population], PREVIOUSYEAR('Date'[Year])),
       CALCULATE([Total Population], PREVIOUSYEAR('Date'[Year]))
   )
   ```

---

### Step 7 — Build the Power BI Dashboard

1. In your workspace, click **+ New item** → **Report**
2. Connect to your Semantic Model
3. Add visuals:
   - **🗺️ Map visual** — Population by Location
   - **📊 Bar chart** — Population by Age Group
   - **📈 Line chart** — Population growth over Time
   - **🍩 Donut chart** — Male vs Female split
   - **🔢 Card visuals** — Total Population, Total Countries
4. Add slicers for Year, Country, Age Group, and Gender

---

## 🧠 Why the Semantic Layer is a Game-Changer

The Semantic Layer is the single most underrated feature in this entire project. Here's why it matters:

| Without Semantic Layer | With Semantic Layer |
|------------------------|---------------------|
| Every report connects directly to raw tables | All reports share one single source of truth |
| Changing a business rule means updating 10 different reports | Change the measure once → all dashboards update instantly |
| Different analysts calculate "Total Population" differently | Everyone uses the same certified definition |
| Performance depends on how well each analyst wrote their query | Measures are pre-optimised once by an engineer |
| New dashboard = write new SQL from scratch | New dashboard = drag and drop from existing Semantic Model |

**The real power: full pipeline automation.** When the pipeline runs (e.g., every Monday at 6 AM):

```
GitHub CSV updates
      ↓
Pipeline copies to Bronze
      ↓
Notebook cleans to Silver
      ↓
Notebook aggregates to Gold
      ↓
Semantic Model refreshes automatically
      ↓
Power BI Dashboard shows new data — no human intervention needed ✅
```

Your stakeholders open their dashboard on Monday morning and see fresh, clean, accurate data — without you lifting a finger.

---

## 📁 Repository Structure

```
WorldPopulation-AzureDataEngineering/
│
├── Dataset/
│   ├── WPP2022_PopulationByAge5GroupSex_Medium_1.csv
│   ├── WPP2022_PopulationByAge5GroupSex_Medium_2.csv
│   ├── WPP2022_PopulationByAge5GroupSex_Medium_3.csv
│   └── metadata.json
│
├── Notebooks/
│   ├── Notebook_BronzeToSilver.ipynb     ← Main cleaning notebook
│   └── Notebook_SilverToGold.ipynb       ← Aggregation notebook
│
├── Pipeline/
│   └── Pipeline_IngestPopulationData/    ← ADF pipeline definition
│
└── README.md                             ← You are here
```

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| **Microsoft Fabric** | Unified analytics platform (workspace, lakehouses, pipelines) |
| **Data Factory** | Pipeline orchestration — Lookup, ForEach, Copy |
| **Delta Lake** | Storage format for all lakehouse tables |
| **Apache Spark / PySpark** | Distributed data processing in notebooks |
| **Data Wrangler** | Visual data transformation with code generation |
| **Power BI** | Interactive dashboard and visualisation |
| **Semantic Model** | Centralised business logic and metrics layer |
| **Outlook** | Pipeline failure email alerting |
| **GitHub** | Source data hosting via HTTP API |

---

## 💡 Key Learnings

- **Medallion Architecture** separates concerns cleanly — raw, clean, and business-ready data each have their own home
- **Excel date corruption** (`5-9` → `09-May`) is a genuine, widespread enterprise data quality problem
- **Dynamic pipelines** using Lookup + ForEach are far more maintainable than hardcoded copy activities
- **Unpivoting** gender columns (wide → long format) dramatically improves Power BI usability
- **The Semantic Layer** is what makes a dashboard truly production-grade — it decouples your data model from your report layer and creates a single, governed source of truth

---

## 🔗 Connect With Me

If you found this project helpful or have questions, feel free to connect:

- 🌐 **Website:** [irshadvaza.tech](https://irshadvaza.tech)
- 💼 **GitHub:** [@irshadvaza](https://github.com/irshadvaza)

---

*Built as part of my Azure Data Engineering portfolio. More projects coming soon!*
