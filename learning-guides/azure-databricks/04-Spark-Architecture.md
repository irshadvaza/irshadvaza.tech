# 📘 Chapter 4 – Apache Spark Architecture

> Understanding How Spark Executes Your Code

---

## 🚀 1️⃣ Introduction

In the previous chapter, we learned:

- What Apache Spark is  
- Why it is fast  
- Where it is used  

Now the most important question:

> What happens internally when you run Spark code?

This chapter explains how Spark works **behind the scenes — step by step**.  

> This is one of the most important topics for **interviews**.

---

## 🧠 2️⃣ High-Level Spark Architecture (One-Line View)

When you run Spark code:

User Code → Driver → Cluster Manager → Executors → Storage


Or visually:

      Driver Program
            |
 -------------------------
 |           |           |
Executor Executor Executor
(Worker) (Worker) (Worker)


Spark follows a **Master–Worker architecture**:

- **Driver = Master**  
- **Executors = Workers**

---

## 🧩 3️⃣ Core Components of Spark Architecture

Spark architecture has **5 main components**:

1. Driver Program  
2. Cluster Manager  
3. Worker Nodes  
4. Executors  
5. Tasks  

Let’s understand each one clearly.

---

## 🧠 4️⃣ Driver Program (The Brain of Spark)

The **Driver** is the main controller of a Spark application.

It is responsible for:

- Converting user code into an execution plan  
- Creating **DAG (Directed Acyclic Graph)**  
- Dividing jobs into stages  
- Sending tasks to executors  
- Collecting results  

### 📌 Example

You write:

df.groupBy("country").count()


The Driver:

- Analyzes the query  
- Creates execution plan  
- Breaks it into stages  
- Sends tasks to executors  

> The driver **does NOT process large data**; it only controls execution.

---

## 🖥 5️⃣ Cluster Manager (Resource Controller)

The **Cluster Manager** manages resources in the cluster.

It decides:

- How many executors to allocate  
- How much memory to assign  
- Where to run the executors  

### Common Cluster Managers

| Cluster Manager | Used In |
|-----------------|---------|
| Standalone | Spark built-in |
| YARN | Hadoop ecosystem |
| Kubernetes | Container-based systems |
| Databricks Runtime | Managed environment |

---

## 🏭 6️⃣ Worker Nodes

Worker nodes are **machines in the cluster**.

Each worker node:

- Hosts **one or more executors**  
- Performs **actual data processing**  
- Communicates with the **driver**  

Think of workers as **physical or virtual machines**.

---

## ⚙ 7️⃣ Executors (The Muscle 💪)

Executors are processes that run on **worker nodes**.  

Responsibilities:

- Executing tasks  
- Performing transformations  
- Reading & writing data  
- Storing intermediate data in memory  

Each executor has:

- CPU cores  
- Memory  
- Task slots  

> Executors are created when a Spark application starts and die when it ends.

---

## 🧵 8️⃣ What is a Task?

A **task** is the **smallest unit of work** in Spark.

Example:

- Dataset has **4 partitions** → Spark creates **4 tasks**  
- Each task processes **one partition**

---

## 🔄 9️⃣ Complete Execution Flow (Step-by-Step)

### Step 1️⃣: User Submits Code

Example:

df.filter("amount > 1000").groupBy("region").sum()


### Step 2️⃣: Driver Creates Logical Plan

- Spark analyzes the query  
- Creates:  
  - Logical plan  
  - Optimized plan  

> Done by **Catalyst Optimizer**

### Step 3️⃣: DAG Creation

- Creates **Directed Acyclic Graph (DAG)**  
- DAG represents **sequence of transformations**

### Step 4️⃣: Job → Stage → Task Breakdown

- **Job:** Triggered by an action (count, collect, write)  
- **Stage:** Group of transformations **without shuffle**  
- **Task:** Smallest unit of execution (per partition)  

### Step 5️⃣: Cluster Manager Allocates Resources

- Provides executors, CPU, memory

### Step 6️⃣: Tasks Sent to Executors

- Driver sends tasks  
- Executors process data and return results

### Step 7️⃣: Final Output Written

- Data written to **ADLS / S3 / Delta Lake / Database**

---

## 📊 1️⃣0️⃣ Job, Stage, and Task (Very Important)

Application
↓
Job
↓
Stage
↓
Task


**Example Scenario:**

df.groupBy("country").count().show()


- Spark creates:  
  - 1 Job  
  - 2 Stages (because of shuffle)  
  - Multiple Tasks (based on partitions)

---

## 🔀 1️⃣1️⃣ What is Shuffle?

Shuffle occurs when **data moves across partitions**.

Examples:

- groupBy  
- join  
- distinct  
- orderBy  

> Shuffle is expensive: network data transfer + disk I/O.  
> Minimizing shuffle improves performance.

---

## 🧱 1️⃣2️⃣ Spark Architecture in Databricks

In Databricks:

Notebook → Driver Node → Worker Nodes → Delta Lake (ADLS)


- Driver runs in **driver node**  
- Executors run in **worker nodes**  
- Data stored in **ADLS**  

> Compute and storage are separated.

---

## 🔐 1️⃣3️⃣ Fault Tolerance in Spark

Spark is **fault tolerant** because of **RDD Lineage**.

- If a partition is lost → Spark recomputes it using the lineage graph  
- No manual recovery required

---

## ⚡ 1️⃣4️⃣ Parallelism in Spark

Parallelism depends on:

- Number of **partitions**  
- Number of **executor cores**  

> More partitions → more tasks → more parallel execution  
> But too many partitions → overhead  
> Balance is important.

---

## 🧠 1️⃣5️⃣ Important Spark Concepts Summary

| Concept | Meaning |
|---------|---------|
| Driver | Controls execution |
| Executor | Executes tasks |
| Cluster Manager | Allocates resources |
| DAG | Execution plan |
| Job | Triggered by action |
| Stage | Group of tasks |
| Task | Smallest unit of work |
| Shuffle | Data movement across partitions |
✅ Chapter 4 is fully structured, GitHub-ready Markdown:

