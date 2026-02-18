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

