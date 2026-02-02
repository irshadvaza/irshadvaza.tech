---
title: Move Data from Blob Storage to SQL Server using Azure Data Factory
date: 2026-02-02
---

# Moving Data from Blob Storage to SQL Server using ADF

This tutorial demonstrates a **beginner-friendly, step-by-step approach** to move data from Azure Blob Storage to SQL Server using Azure Data Factory (ADF).

## Prerequisites
- Azure subscription  
- Storage account with data  
- SQL Server or Azure SQL Database

## Steps

### Step 1: Create a Data Factory
1. Navigate to Azure Portal → Create Data Factory → Fill in details.

### Step 2: Create Linked Services
- Connect Blob Storage and SQL Server in **Linked Services**.

### Step 3: Build a Pipeline
- Add **Copy Data activity**:
  - Source: Blob Storage  
  - Sink: SQL Server

### Step 4: Trigger & Monitor
- Run the pipeline manually and monitor execution in ADF portal.

## Results
- Data successfully moved from Blob Storage to SQL Server.
- Pipeline can now be scheduled or triggered automatically.

## Key Takeaways
- ADF simplifies ETL processes without heavy coding.
- Linked Services and Datasets are key concepts for integration.

