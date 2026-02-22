# 🚀 Chapter 5: ForEach Loop in Azure Data Factory (Control Flow Mastery)

---

# 🎯 Objective of This Chapter

In this chapter, you will learn:

- What is ForEach activity
- Why ForEach is used in enterprise pipelines
- How to loop through array parameters
- How to use variables inside loop
- How to use dynamic expressions
- How to debug and monitor loop execution

By the end of this chapter, you will understand how to process multiple values dynamically using a single pipeline.

---

# 🧠 What is ForEach Activity?

ForEach activity allows you to:

✅ Iterate over an array  
✅ Execute activities multiple times  
✅ Process dynamic values  
✅ Build scalable pipelines  

Instead of creating 4 activities for 4 countries...

You create:

✔️ 1 ForEach  
✔️ 1 Logic  
✔️ It runs 4 times automatically  

---

# 🏢 Real Enterprise Scenario

Imagine you have operations in multiple countries:

- UAE
- UK
- USA
- India

Every day you must:

- Extract data for each country
- Load into Data Lake
- Process individually

Instead of building separate pipelines…

We use ForEach loop.

---

# 🏗️ Step 1: Create New Pipeline

Go to:

Author → + → Pipeline

Rename:

```
pl_foreach_country_processing
```

---

# ⚙️ Step 2: Create Pipeline Parameter (Array Type)

Click blank canvas → Parameters tab

Create:

| Name | Type | Default Value |
|------|------|---------------|
| p_countries | Array | ["UAE","UK","USA","India"] |

Now pipeline can loop over this array.

This is powerful and scalable.

---

# 🔁 Step 3: Add ForEach Activity

From Activities panel:

Drag:

```
ForEach
```

Rename:

```
foreach_country
```

---

# ⚙️ Step 4: Configure ForEach Items

Click ForEach → Settings tab

In Items:

Click **Add dynamic content**

Enter:

```
@pipeline().parameters.p_countries
```

Now ForEach will iterate over each country.

---

# 🧰 Step 5: Create Variable

Click on blank canvas → Variables tab

Create:

| Name | Type |
|------|------|
| country | String |

This variable will store current loop value.

---

# 🔄 Step 6: Add Set Variable Activity Inside Loop

Double-click ForEach activity to enter loop container.

Drag:

```
Set Variable
```

Rename:

```
set_current_country
```

Configure:

- Variable name: `country`
- Value (Dynamic Content):

```
@item()
```

Explanation:

- `@item()` represents current value in loop
- In first iteration → UAE
- Second → UK
- Third → USA
- Fourth → India

---

# 🧪 Step 7: Debug the Pipeline

Click:
```
Debug
```

Go to:

Monitor → Pipeline Runs

Click on pipeline run → Activity runs

You will see:

ForEach executed 4 times.

Inside each iteration:

```
Iteration 1 → UAE
Iteration 2 → UK
Iteration 3 → USA
Iteration 4 → India
```

Check Output of Set Variable:

You will see:

```
"value": "UAE"
"value": "UK"
"value": "USA"
"value": "India"
```

Congratulations 🎉  
Your loop is working correctly.

---

# 🧠 What Happens Internally?

Pipeline receives:

```
["UAE","UK","USA","India"]
```

ForEach splits into:

```
Iteration 1 → item() = "UAE"
Iteration 2 → item() = "UK"
Iteration 3 → item() = "USA"
Iteration 4 → item() = "India"
```

Set Variable captures each value.

---

# 🔥 Important: Sequential vs Parallel Execution

In ForEach Settings:

You will see:

- Sequential
- Batch count

If Sequential = OFF

ADF runs iterations in parallel (default max 20).

If Sequential = ON

ADF runs one by one.

Enterprise Recommendation:

- Use parallel for independent tasks
- Use sequential for dependent processing

---

# 📊 Enterprise Use Cases of ForEach

✔️ Process multiple countries  
✔️ Process multiple tables  
✔️ Process multiple files  
✔️ Loop over metadata table  
✔️ Call stored procedure for each record  
✔️ Copy multiple folders  

ForEach is core building block of dynamic pipelines.

---

# 🏗️ Advanced Enterprise Example

Imagine instead of simple array, you have:

```
[
  {"country":"UAE","currency":"AED"},
  {"country":"UK","currency":"GBP"},
  {"country":"USA","currency":"USD"}
]
```

Inside ForEach:

Access values:

```
@item().country
@item().currency
```

This allows complex enterprise processing.

---

# 🧪 Debugging Tips

If loop not running:

✔️ Check parameter type is Array  
✔️ Validate dynamic expression  
✔️ Confirm no spelling mistakes  
✔️ Check Monitor output JSON  

Always inspect:

Activity Output → Input/Output tab

---

# ❌ Common Mistakes

❌ Creating parameter as String instead of Array  
❌ Forgetting @item() expression  
❌ Trying to access variable before set  
❌ Not enabling dynamic content  

---

# 🏢 Enterprise Pattern: ForEach + Copy Activity

Real production flow:

```
Lookup (Get list of tables)
        ↓
ForEach (Loop tables)
        ↓
Copy Activity
        ↓
Log Status
```

One pipeline handles 50 tables dynamically.

---

# 📈 Scaling Example

Instead of:

```
["UAE","UK","USA","India"]
```

In production, array may come from:

- SQL Lookup
- Metadata table
- REST API response
- Get Metadata child items

ForEach works with any array.

---

# 🏁 What You Built

You successfully built:

✔️ Array Parameter  
✔️ ForEach Loop  
✔️ Variable Handling  
✔️ Dynamic Expression using @item()  
✔️ Debugged multiple iterations  
✔️ Viewed output for each country  

You now understand dynamic looping in Azure Data Factory.

---

# 🚀 Coming Next in Chapter 6

Next chapter will cover:

- Lookup Activity
- Reading from Control Table
- Combining Lookup + ForEach
- Real Metadata-Driven Enterprise Pipeline
- Processing 50+ Tables with One Pipeline

This is senior ADF developer level.

---

# 🎓 Final Summary

ForEach activity allows you to:

- Loop over arrays
- Process multiple items dynamically
- Reduce duplicate pipelines
- Build scalable enterprise solutions

Instead of repeating logic…

You build once and loop intelligently.

---

✨ Congratulations! You have completed Chapter 5 – ForEach Loop Mastery in Azure Data Factory.
