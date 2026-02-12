📘 Chapter 4 – Apache Spark Architecture

Understanding How Spark Executes Your Code

🚀 1️⃣ Introduction

In the previous chapter, we learned:

What Apache Spark is

Why it is fast

Where it is used

Now the most important question:

What happens internally when you run Spark code?

This chapter explains how Spark works behind the scenes — step by step.

This is one of the most important topics for interviews.

🧠 2️⃣ High-Level Spark Architecture (One-Line View)

When you run Spark code:

User Code → Driver → Cluster Manager → Executors → Storage


Or visually:

          Driver Program
                |
     -------------------------
     |           |           |
 Executor     Executor     Executor
 (Worker)     (Worker)     (Worker)


Spark follows a Master–Worker architecture.

Driver = Master

Executors = Workers

🧩 3️⃣ Core Components of Spark Architecture

Spark architecture has 5 main components:

Driver Program

Cluster Manager

Worker Nodes

Executors

Tasks

Let’s understand each one clearly.

🧠 4️⃣ Driver Program (The Brain of Spark)

The Driver is the main controller of a Spark application.

It is responsible for:

Converting user code into execution plan

Creating DAG (Directed Acyclic Graph)

Dividing jobs into stages

Sending tasks to executors

Collecting results

📌 Example

You write:

df.groupBy("country").count()


The Driver:

Analyzes the query

Creates execution plan

Breaks it into stages

Sends tasks to executors

The driver does NOT process large data.
It only controls execution.

🖥 5️⃣ Cluster Manager (Resource Controller)

The Cluster Manager manages resources in the cluster.

It decides:

How many executors to allocate

How much memory to assign

Where to run the executors

Common Cluster Managers
Cluster Manager	Used In
Standalone	Spark built-in
YARN	Hadoop ecosystem
Kubernetes	Container-based systems
Databricks Runtime	Managed environment
🏭 6️⃣ Worker Nodes

Worker nodes are machines in the cluster.

Each worker node:

Hosts one or more executors

Performs actual data processing

Communicates with driver

Think of workers as physical/virtual machines.

⚙ 7️⃣ Executors (The Muscle 💪)

Executors are processes that run on worker nodes.

They are responsible for:

Executing tasks

Performing transformations

Reading & writing data

Storing intermediate data in memory

Each executor has:

CPU cores

Memory

Task slots

Important Point

Executors are created when a Spark application starts
Executors die when application ends

🧵 8️⃣ What is a Task?

A task is the smallest unit of work in Spark.

Example:

If a dataset has 4 partitions → Spark creates 4 tasks.

Each task processes one partition.

🔄 9️⃣ Complete Execution Flow (Step-by-Step)

Let’s understand what happens when you run a Spark job.

Step 1️⃣: User Submits Code

Example:

df.filter("amount > 1000").groupBy("region").sum()

Step 2️⃣: Driver Creates Logical Plan

Spark analyzes the query.

It creates:

Logical plan

Optimized plan

This is done by Catalyst Optimizer.

Step 3️⃣: DAG Creation

Spark creates a:

Directed Acyclic Graph (DAG)

DAG represents the sequence of transformations.

Step 4️⃣: Job → Stage → Task Breakdown

Spark divides execution into:

Job

Stages

Tasks

🔹 Job

Triggered by an action (count, collect, write)

🔹 Stage

Group of transformations without shuffle

🔹 Task

Smallest unit of execution (per partition)

Step 5️⃣: Cluster Manager Allocates Resources

Cluster Manager provides:

Executors

CPU

Memory

Step 6️⃣: Tasks Sent to Executors

Driver sends tasks.

Executors:

Process data

Return results

Step 7️⃣: Final Output Written

Data is written to:

ADLS

S3

Delta Lake

Database

📊 1️⃣0️⃣ Job, Stage, and Task (Very Important)

Understanding this is critical.

Application
   ↓
Job
   ↓
Stage
   ↓
Task

Example Scenario

You run:

df.groupBy("country").count().show()


Spark creates:

1 Job

2 Stages (because of shuffle)

Multiple Tasks (based on partitions)

🔀 1️⃣1️⃣ What is Shuffle?

Shuffle occurs when data moves across partitions.

Example:

groupBy

join

distinct

orderBy

Shuffle is expensive because:

Data moves across network

Disk I/O increases

Minimizing shuffle improves performance.

🧱 1️⃣2️⃣ Spark Architecture in Databricks

In Databricks:

Notebook → Driver Node → Worker Nodes → Delta Lake (ADLS)


Driver runs in driver node

Executors run in worker nodes

Data stored in ADLS

Important:

Compute and Storage are separated

🔐 1️⃣3️⃣ Fault Tolerance in Spark

Spark is fault tolerant because of:

RDD Lineage

If a partition is lost:

Spark recomputes it using lineage graph

No manual recovery required

⚡ 1️⃣4️⃣ Parallelism in Spark

Parallelism depends on:

Number of partitions

Number of executor cores

More partitions → More tasks → More parallel execution

But too many partitions → Overhead

Balance is important.

🧠 1️⃣5️⃣ Important Spark Concepts Summary
Concept	Meaning
Driver	Controls execution
Executor	Executes tasks
Cluster Manager	Allocates resources
DAG	Execution plan
Job	Triggered by action
Stage	Group of tasks
Task	Smallest unit of work
Shuffle	Data movement across partitions
