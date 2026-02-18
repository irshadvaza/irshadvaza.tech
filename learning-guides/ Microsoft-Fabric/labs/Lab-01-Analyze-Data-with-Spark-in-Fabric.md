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
