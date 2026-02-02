---
title: Build an End-to-End ML Pipeline in Azure Databricks
date: 2026-02-02
---

# Building an End-to-End ML Pipeline in Azure Databricks

This tutorial shows how to create a complete machine learning pipeline in Databricks with Python and Delta Lake.

## Steps

### Step 1: Load Data
```python
df = spark.read.format("delta").load("/mnt/gold/transactions")
df.show()
