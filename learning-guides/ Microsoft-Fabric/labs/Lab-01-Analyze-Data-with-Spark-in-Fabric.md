
🧪 Lab 01 – Analyze Data with Apache Spark in Fabric
🎯 Lab Objective

In this lab, you will:

Create a Fabric workspace

Create a Lakehouse

Upload data files

Create a Notebook

Use PySpark to analyze data

Transform and save data

Create Delta tables

Run SQL queries

Visualize data using charts

⏱ Estimated Time

45 Minutes

📌 Prerequisites

Access to a Fabric-enabled tenant

Internet connection

Fabric login credentials

🏗 Part 1 – Create Workspace

Open Fabric portal:
👉 https://app.fabric.microsoft.com

Sign in.

From left menu, select Workspaces.

Click New Workspace.

Enter a name (example: SparkLabWorkspace).

In Advanced settings, choose a license mode:

Trial

Premium

Fabric capacity

Click Create.

✅ Workspace is ready.

🏞 Part 2 – Create Lakehouse

In left menu, click Create
(If not visible, click the ... first.)

Under Data Engineering, select Lakehouse.

Enter a name:
SalesLakehouse

Make sure:

Lakehouse schemas (Public Preview) = Disabled


Click Create.

Fabric creates storage automatically in:

OneLake

📥 Part 3 – Upload Data Files
Step 1 – Download Data

Download dataset:

https://github.com/MicrosoftLearning/dp-data/raw/main/orders.zip


Extract the file.

You should see:

orders/
   ├── 2019.csv
   ├── 2020.csv
   └── 2021.csv

Step 2 – Upload to Lakehouse

Open your Lakehouse.

In Explorer pane, click ... next to Files

Select Upload → Upload Folder

Choose the orders folder

Upload

Verify:

Files/
   └── orders/
       ├── 2019.csv
       ├── 2020.csv
       └── 2021.csv

📓 Part 4 – Create Notebook

Click Create

Select Notebook

Rename it to:

Sales_Data_Exploration

Add Markdown Title

Convert first cell to Markdown.

Add:

# Sales Order Data Exploration
This notebook explores sales order data using PySpark.

🔥 Part 5 – Create Spark DataFrame
Load 2019 Data
df = spark.read.format("csv") \
    .option("header","false") \
    .load("Files/orders/2019.csv")

display(df)

Define Schema (Best Practice)
from pyspark.sql.types import *

orderSchema = StructType([
    StructField("SalesOrderNumber", StringType()),
    StructField("SalesOrderLineNumber", IntegerType()),
    StructField("OrderDate", DateType()),
    StructField("CustomerName", StringType()),
    StructField("Email", StringType()),
    StructField("Item", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("UnitPrice", FloatType()),
    StructField("Tax", FloatType())
])

df = spark.read.format("csv") \
    .schema(orderSchema) \
    .load("Files/orders/*.csv")

display(df)


Now all 3 years are loaded.

🔍 Part 6 – Explore Data
Filter Columns
customers = df.select("CustomerName", "Email")

print(customers.count())
print(customers.distinct().count())

display(customers.distinct())

Filter Specific Product
customers = df.select("CustomerName", "Email") \
              .where(df["Item"] == "Road-250 Red, 52")

display(customers.distinct())

📊 Part 7 – Aggregation
Quantity per Product
productSales = df.select("Item", "Quantity") \
                 .groupBy("Item") \
                 .sum()

display(productSales)

Orders per Year
from pyspark.sql.functions import *

yearlySales = df.select(year(col("OrderDate")).alias("Year")) \
                .groupBy("Year") \
                .count() \
                .orderBy("Year")

display(yearlySales)

🔄 Part 8 – Transform Data
from pyspark.sql.functions import *

transformed_df = df.withColumn("Year", year(col("OrderDate"))) \
                   .withColumn("Month", month(col("OrderDate"))) \
                   .withColumn("FirstName", split(col("CustomerName"), " ").getItem(0)) \
                   .withColumn("LastName", split(col("CustomerName"), " ").getItem(1))

display(transformed_df.limit(5))

💾 Part 9 – Save as Parquet
transformed_df.write.mode("overwrite") \
    .parquet("Files/transformed_data/orders")

print("Transformed data saved!")


Reload:

orders_df = spark.read.format("parquet") \
    .load("Files/transformed_data/orders")

display(orders_df)

🚀 Part 10 – Partition Data
orders_df.write.partitionBy("Year","Month") \
    .mode("overwrite") \
    .parquet("Files/partitioned_data")

print("Partitioned data saved!")


Load 2021 only:

orders_2021_df = spark.read.format("parquet") \
    .load("Files/partitioned_data/Year=2021/Month=*")

display(orders_2021_df)

🏛 Part 11 – Create Delta Table
df.write.format("delta") \
    .saveAsTable("salesorders")


Check table:

spark.sql("DESCRIBE EXTENDED salesorders").show(truncate=False)

🧾 Query Using SQL
%%sql
SELECT YEAR(OrderDate) AS OrderYear,
       SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue
FROM salesorders
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear;

📈 Part 12 – Visualize with Matplotlib
from matplotlib import pyplot as plt

df_sales = spark.sql("""
SELECT CAST(YEAR(OrderDate) AS STRING) AS OrderYear,
       SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue
FROM salesorders
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear
""").toPandas()

plt.figure(figsize=(8,4))
plt.bar(df_sales["OrderYear"], df_sales["GrossRevenue"])
plt.title("Revenue by Year")
plt.xlabel("Year")
plt.ylabel("Revenue")
plt.show()

🎨 Using Seaborn
import seaborn as sns
sns.set_theme(style="whitegrid")

sns.lineplot(x="OrderYear",
             y="GrossRevenue",
             data=df_sales)

plt.show()

🧠 What You Learned

In this lab you:

✅ Created workspace
✅ Created Lakehouse
✅ Uploaded files
✅ Used PySpark
✅ Filtered and grouped data
✅ Transformed data
✅ Saved Parquet files
✅ Partitioned data
✅ Created Delta table
✅ Ran SQL queries
✅ Built visualizations

🏆 You Now Understand

Spark DataFrames

Delta tables

Lakehouse storage

Partitioning strategy

SQL in notebooks

Basic data visualization
