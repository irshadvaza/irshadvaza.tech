# 🏗 Part 1 – Create a Fabric Workspace

A workspace is a container where all your Fabric items (Lakehouse, Notebook, Pipelines, etc.) will live.

### Step 1 – Open Fabric Portal

Go to:

https://app.fabric.microsoft.com

Sign in with your account.

---

### Step 2 – Create New Workspace

1. From the left menu, click **Workspaces**
2. Click **+ New Workspace**
3. Enter a name:

   ```
   SparkLabWorkspace
   ```

4. Expand **Advanced settings**
5. Select a License mode:
   - Trial
   - Premium
   - Fabric Capacity (if available)

6. Click **Create**

✅ Your workspace is now ready.

---

# 🏞 Part 2 – Create a Lakehouse

A Lakehouse combines the power of a data lake and a data warehouse.

All data in Fabric is stored in:

Microsoft OneLake (Unified storage layer)

---

### Step 1 – Create Lakehouse

1. Inside your new workspace, click **+ New**
2. Select **Lakehouse**
3. Enter name:

   ```
   SalesLakehouse
   ```

4. Make sure:

   ```
   Lakehouse schemas (Public Preview) = Disabled
   ```

5. Click **Create**

Fabric will automatically provision storage.

---

### ✅ Verify Lakehouse Structure

After creation, you should see:

```
SalesLakehouse
 ├── Tables
 └── Files
```

- **Tables** → Managed Delta tables
- **Files** → Raw data storage

---

## 🧠 What You Learned in This Part

- What a Workspace is
- How to create a Workspace
- What a Lakehouse is
- How to create a Lakehouse
- Understanding Tables vs Files section

---

# 📥 Part 3 – Upload Data Files to the Lakehouse

In this section, we will:

- Download sample sales data
- Upload it into the Lakehouse
- Verify file structure

---

## 📦 Step 1 – Download the Dataset

Download the sample dataset from:

https://github.com/MicrosoftLearning/dp-data/raw/main/orders.zip

After downloading:

1. Extract the ZIP file
2. You should see a folder named:

   ```
   orders
   ```

Inside the folder:

```
orders/
 ├── 2019.csv
 ├── 2020.csv
 └── 2021.csv
```

Each file contains sales order data for one year.

---

## ⬆ Step 2 – Upload Files to Lakehouse

Now we will upload this folder to Fabric.

1. Open your **SalesLakehouse**
2. In the left Explorer pane, find **Files**
3. Click the `...` (three dots) next to Files
4. Select:

   ```
   Upload → Upload Folder
   ```

5. Choose the **orders** folder
6. Click **Upload**

Wait until upload completes.

---

## ✅ Step 3 – Verify Upload

After upload, your Lakehouse should look like:

```
Files/
 └── orders/
     ├── 2019.csv
     ├── 2020.csv
     └


# 📓 Part 4 – Create Notebook and Load Data with Spark

In this section, you will:

- Create a Notebook
- Add Markdown documentation
- Load CSV files using PySpark
- Create a Spark DataFrame

---

## 🆕 Step 1 – Create a Notebook

1. Inside your workspace, click **+ New**
2. Select **Notebook**
3. Rename the notebook to:

   ```
   Sales_Data_Exploration
   ```

Now you are inside the Fabric Notebook editor.

---

## 📝 Step 2 – Add Notebook Title (Markdown Cell)

1. Select the first cell
2. Change the cell type to **Markdown**
3. Paste the following:

```markdown
# Sales Order Data Exploration

This notebook analyzes sales data using Apache Spark in Microsoft Fabric.
```

4. Click **Run** to render the Markdown.

---

## 🔥 Step 3 – Load CSV Data into Spark DataFrame

Now create a new code cell and paste:

```python
df = spark.read.format("csv") \
    .option("header", "false") \
    .load("Files/orders/2019.csv")

display(df)
```

Click **Run**.

You will see raw data loaded into a Spark DataFrame.

---

## 📌 What Happened?

- Spark accessed the Lakehouse storage
- It read the CSV file
- It created a distributed DataFrame
- `display()` shows interactive results

---

## 🚀 Step 4 – Load All Years at Once

Instead of loading one file, we can load all years:

```python
df = spark.read.format("csv") \
    .option("header", "false") \
    .load("Files/orders/*.csv")

display(df)
```

The `*` means:
Load all CSV files inside the folder.

---

## 📊 Step 5 – Check Record Count

```python
print("Total Records:", df.count())
```

This confirms all data is loaded.

---

## 🧠 Why Spark DataFrame?

A Spark DataFrame:

- Is distributed across multiple nodes
- Handles large-scale data
- Supports SQL-like operations
- Is optimized for performance

---

## 🧠 What You Learned in This Part

- How to create a Notebook
- Difference between Markdown and Code cells
- How to load CSV files into Spark
- How to create a Spark DataFrame
- How to load multiple files using wildcard

---

# 🧩 Part 5 – Define Schema and Explore Data

In real-world projects, we should NOT rely on automatic schema detection.

Instead, we define the schema manually to:

- Ensure correct data types
- Improve performance
- Avoid data quality issues
- Follow enterprise standards

---

## 🏗 Step 1 – Define Schema

Create a new code cell and paste:

```python
from pyspark.sql.types import *

orderSchema = StructType([
    StructField("SalesOrderNumber", StringType(), True),
    StructField("SalesOrderLineNumber", IntegerType(), True),
    StructField("OrderDate", DateType(), True),
    StructField("CustomerName", StringType(), True),
    StructField("Email", StringType(), True),
    StructField("Item", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("UnitPrice", FloatType(), True),
    StructField("Tax", FloatType(), True)
])
```

This defines the structure of our dataset.

---

## 🔄 Step 2 – Load Data Using Defined Schema

```python
df = spark.read.format("csv") \
    .schema(orderSchema) \
    .load("Files/orders/*.csv")

display(df)
```

Now:

- Data types are properly assigned
- Dates are treated as Date type
- Numbers are numeric (not strings)

---

## 📊 Step 3 – View Schema

```python
df.printSchema()
```

You should see:

- String columns
- Integer columns
- Date column
- Float columns

This confirms schema is applied correctly.

---

# 🔍 Step 4 – Basic Data Exploration

---

## 📌 Total Records

```python
print("Total Records:", df.count())
```

---

## 📌 View Sample Data

```python
display(df.limit(10))
```

---

## 📌 Select Specific Columns

```python
customers = df.select("CustomerName", "Email")

display(customers.limit(10))
```

---

## 📌 Count Distinct Customers

```python
print("Total Customers:", customers.distinct().count())
```

---

# 🎯 Step 5 – Filter Data

Example: Show orders for a specific product.

```python
road_bike_orders = df.filter(df["Item"] == "Road-250 Red, 52")

display(road_bike_orders)
```

Filtering is one of the most common Spark operations.

---

# 📈 Step 6 – Aggregate Data

Example: Total quantity sold per product.

```python
product_sales = df.groupBy("Item") \
                  .sum("Quantity") \
                  .orderBy("sum(Quantity)", ascending=False)

display(product_sales)
```

This groups data and calculates totals.

---

# 📅 Step 7 – Extract Year from Order Date

```python
from pyspark.sql.functions import year

yearly_orders = df.withColumn("Year", year("OrderDate")) \
                  .groupBy("Year") \
                  .count() \
                  .orderBy("Year")

display(yearly_orders)
```

Now we understand how many orders happened per year.

---

# 🧠 What You Learned in This Part

- Why defining schema is important
- How to create a StructType schema
- How to apply schema while reading data
- How to explore data using:
  - select()
  - filter()


# 🔄 Part 6 – Transform Data and Create New Columns

In this section, we will:

- Create calculated columns
- Extract Year and Month
- Split customer name into First and Last name
- Calculate total sales amount
- Prepare data for analytics

This is the core job of a Data Engineer.

---

## 🧮 Step 1 – Import Required Functions

Create a new code cell:

```python
from pyspark.sql.functions import year, month, split, col
```

---

## 📅 Step 2 – Extract Year and Month from OrderDate

```python
transformed_df = df.withColumn("Year", year(col("OrderDate"))) \
                   .withColumn("Month", month(col("OrderDate")))

display(transformed_df.limit(5))
```

Now we have:

- Year column
- Month column

This is useful for reporting and partitioning.

---

## 👤 Step 3 – Split Customer Name

Currently, CustomerName is a single column.

We split it into:

- FirstName
- LastName

```python
transformed_df = transformed_df.withColumn(
                    "FirstName",
                    split(col("CustomerName"), " ").getItem(0)
                 ).withColumn(
                    "LastName",
                    split(col("CustomerName"), " ").getItem(1)
                 )

display(transformed_df.limit(5))
```

Now data is more structured.

---

## 💰 Step 4 – Create Total Sales Column

We calculate total sales per row:

```
TotalAmount = (UnitPrice × Quantity) + Tax
```

```python
transformed_df = transformed_df.withColumn(
                    "TotalAmount",
                    (col("UnitPrice") * col("Quantity")) + col("Tax")
                 )

display(transformed_df.limit(5))
```

Now each record has revenue information.

---

## 📊 Step 5 – Verify New Columns

Check schema again:

```python
transformed_df.printSchema()
```

You should now see:

- Year
- Month
- FirstName
- LastName
- TotalAmount

---

# 🧠 Why Transform Data?

Raw data is not ready for analytics.

We transform to:

- Improve readability
- Enable reporting
- Optimize performance
- Prepare for partitioning
- Create business-ready fields

---

# 🏆 Real-World Best Practice

In enterprise systems:

- Raw data → Bronze layer
- Cleaned data → Silver layer
- Aggregated data → Gold layer

In this lab:

- CSV files = Bronze
- transformed_df = Silver

---

## 🧠 What You Learned in This Part

- How to create new columns using withColumn()
- How to extract date components
- How to split string columns
- How to create calculated business metrics
- Why transformations are essential in data engineering

---


# 💾 Part 7 – Save Data as Parquet and Partition It

Parquet is a columnar storage format:

- Highly efficient
- Supports compression
- Works well with Spark
- Recommended for large-scale analytics

Partitioning further improves performance by allowing Spark to read only relevant data.

---

## 📦 Step 1 – Save Transformed Data as Parquet

```python
transformed_df.write.mode("overwrite") \
    .parquet("Files/transformed_data/orders")

print("Transformed data saved!")
```

✅ This saves your data in a Parquet format inside your Lakehouse.

---

## 🔄 Step 2 – Read Parquet Data

```python
orders_df = spark.read.format("parquet") \
    .load("Files/transformed_data/orders")

display(orders_df.limit(5))
```

You now have a Spark DataFrame with your Parquet data.

---

## 🗂 Step 3 – Save Data Partitioned by Year and Month

Partitioning organizes files into folders:

```python
orders_df.write.partitionBy("Year", "Month") \
    .mode("overwrite") \
    .parquet("Files/partitioned_data")

print("Partitioned data saved!")
```

After this, the folder structure looks like:

```
partitioned_data/
 ├── Year=2019/
 │    ├── Month=1/
 │    ├── Month=2/
 │    └── ...
 ├── Year=2020/
 └── Year=2021/
```

---

## 🔍 Step 4 – Read Partitioned Data

```python
orders_2021_df = spark.read.format("parquet") \
    .load("Files/partitioned_data/Year=2021/Month=*")

display(orders_2021_df.limit(5))
```

✅ You now have data filtered by Year=2021 automatically, thanks to partitioning.

---

# 🧠 Why Use Parquet and Partitioning?

- Columnar storage → faster queries
- Compression → smaller storage size
- Partitioning → reads only necessary data
- Industry standard for data lakehouses

---

## 🧠 What You Learned in This Part

- How to save a Spark DataFrame as Parquet
- How to read Parquet data
- How to partition data for performance
- How to query partitioned data efficiently

---

# 🏆 Pro Tip

Partition by fields that are frequently filtered in analytics, such as:

- Year
- Month
- Region
- Product Category

This reduces data scanning and speeds up queries.

---


# 🧩 Part 8 – Create Tables and Run SQL Queries in Fabric

In this part, you will:

- Create a Delta table from a Spark DataFrame
- Use Spark SQL to query the table
- Explore %%sql magic commands in notebooks
- Prepare data for analytics and reporting

---

## 🏗 Step 1 – Create a Delta Table

Delta tables provide:

- ACID transactions
- Schema enforcement
- Versioning
- SQL compatibility

```python
# Create a managed Delta table
transformed_df.write.format("delta") \
    .saveAsTable("salesorders")

# Verify table
spark.sql("DESCRIBE EXTENDED salesorders").show(truncate=False)
```

✅ Now `salesorders` table is available in your Lakehouse metastore.

---

## 🔄 Step 2 – Load Table into DataFrame

```python
df_sales = spark.sql("SELECT * FROM salesorders LIMIT 1000")

display(df_sales)
```

You can query it like any Spark DataFrame.

---

## 📊 Step 3 – Run SQL Queries in Notebook

Fabric notebooks support **%%sql magic** to run SQL directly.

```sql
%%sql
SELECT YEAR(OrderDate) AS OrderYear,
       SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue,
       COUNT(DISTINCT SalesOrderNumber) AS TotalOrders
FROM salesorders
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear;
```

✅ Output appears immediately below the cell as a table.

---

## 💡 Step 4 – Filter and Aggregate

Example: Total sales for a specific item:

```sql
%%sql
SELECT CustomerName,
       SUM((UnitPrice * Quantity) + Tax) AS CustomerRevenue
FROM salesorders
WHERE Item = 'Road-250 Red, 52'
GROUP BY CustomerName
ORDER BY CustomerRevenue DESC
LIMIT 10;
```

This shows top 10 customers for a product.

---

## 📈 Step 5 – Visualize SQL Query Results

1. Run the SQL query
2. Click **+ New chart** in the result pane
3. Customize chart settings:
   - Chart type: Bar
   - X-axis: OrderYear
   - Y-axis: GrossRevenue
   - Aggregation: Sum
   - Missing values: Display as 0

✅ Now you have visualized yearly revenue directly from SQL results.

---

## 🔀 Step 6 – Combine SQL and Spark DataFrame

```python
# Use SQL query result as Spark DataFrame
df_yearly = spark.sql("""
    SELECT YEAR(OrderDate) AS OrderYear,
           SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue
    FROM salesorders
    GROUP BY YEAR(OrderDate)
""")

# Convert to Pandas for advanced plotting
df_pandas = df_yearly.toPandas()

display(df_pandas)
```

This enables hybrid analysis:

- SQL for querying
- Spark DataFrame for transformations
- Pandas for visualization

---

# 🧠 Why Use Delta + SQL?

- Delta tables combine the power of a DataFrame with a relational table
- SQL makes it easy for analysts to query
- Supports advanced analytics and BI tools like Power BI

---

## 🧠 What You Learned in This Part

- How to create a Delta table from Spark DataFrame
- How to query Delta tables using Spark SQL
- How to use %%sql magic in Fabric notebooks
- How to visualize SQL query results
- How to integrate SQL and Spark transformations

---

# 🏆 Pro Tip

- Always use Delta tables in Fabric for production
- Use descriptive table names and maintain schema versioning
- Partition large tables for performance

---


# 📊 Part 9 – Advanced Visualization with Matplotlib & Seaborn

Visualizations help uncover patterns and insights faster than tables of numbers.

In this part, we will:

- Use Matplotlib for bar charts, line charts, and subplots
- Use Seaborn for elegant statistical plots
- Combine SQL and Spark data for visualization
- Customize charts for professional reporting

---

## 🏗 Step 1 – Import Libraries

```python
from matplotlib import pyplot as plt
import seaborn as sns
```

---

## 📈 Step 2 – Prepare Data

Use previously created Spark SQL query:

```python
sqlQuery = """
SELECT CAST(YEAR(OrderDate) AS CHAR(4)) AS OrderYear,
       SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue,
       COUNT(DISTINCT SalesOrderNumber) AS TotalOrders
FROM salesorders
GROUP BY CAST(YEAR(OrderDate) AS CHAR(4))
ORDER BY OrderYear
"""

df_spark = spark.sql(sqlQuery)
df_sales = df_spark.toPandas()  # Matplotlib & Seaborn require Pandas
```

---

## 📊 Step 3 – Bar Chart with Matplotlib

```python
plt.bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'], color='orange')
plt.title('Gross Revenue by Year')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
```

✅ Simple bar chart showing yearly revenue.

---

## 📈 Step 4 – Create Figure & Subplots

```python
fig, ax = plt.subplots(1, 2, figsize=(12,4))

# Bar chart for revenue
ax[0].bar(df_sales['OrderYear'], df_sales['GrossRevenue'], color='green')
ax[0].set_title('Revenue by Year')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Revenue')

# Pie chart for number of orders
ax[1].pie(df_sales['TotalOrders'], labels=df_sales['OrderYear'], autopct='%1.1f%%')
ax[1].set_title('Orders per Year')

fig.suptitle('Sales Overview')
plt.show()
```

✅ One figure, two charts – professional style.

---

## 🎨 Step 5 – Visualize with Seaborn

### Bar Chart

```python
sns.set_theme(style="whitegrid")
ax = sns.barplot(x='OrderYear', y='GrossRevenue', data=df_sales, palette='coolwarm')
ax.set_title('Gross Revenue by Year')
plt.show()
```

### Line Chart

```python
ax = sns.lineplot(x='OrderYear', y='GrossRevenue', data=df_sales, marker='o')
ax.set_title('Revenue Trend')
plt.show()
```

Seaborn provides:

- Beautiful default themes
- Easy color palettes
- Statistical plot support

---

## 🔍 Step 6 – Customize Seaborn Chart

```python
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8,4))
ax = sns.barplot(x='OrderYear', y='GrossRevenue', data=df_sales, palette='viridis')
ax.set_title('Annual Revenue')
ax.set_xlabel('Year')
ax.set_ylabel('Revenue')
plt.xticks(rotation=45)
plt.show()
```

✅ Customized plot for professional dashboards.

---

## 🧠 Why This Matters

- Analysts prefer charts over raw data
- Charts highlight trends quickly
- Seaborn + Matplotlib allows fine control for presentations
- Works seamlessly with Spark + SQL pipelines in Fabric

---

## 🧠 What You Learned in This Part

- Convert Spark SQL results to Pandas for plotting
- Create bar charts, line charts, and pie charts
- Use subplots for multi-chart dashboards
- Customize colors, titles, and grids
- Apply Seaborn themes for polished visualizations

---

# 🏆 Pro Tip

- Always convert Spark DataFrame to Pandas for plotting
- Use subplots for multiple related charts
- Pick meaningful colors and labels
- Keep charts clean and readable for presentations

---

