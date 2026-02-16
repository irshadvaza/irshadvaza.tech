# 📘 Chapter 3 – Measures of Central Tendency

---

## 🎯 Why Measures of Central Tendency Matter

In statistics, **central tendency** helps us understand the **“center” or “typical” value** of a dataset.  

- Simplifies large datasets  
- Summarizes data with a single representative value  
- Forms the basis for further analysis like variance, standard deviation, or probability  

**Example:**  

A teacher has marks of 5 students:  
`[70, 85, 90, 60, 95]`  

Instead of analyzing all numbers, we can use **mean, median, or mode** to understand the overall performance.

---

# 1️⃣ Mean (Average)

### 📌 Definition
The **mean** is the sum of all values divided by the total number of values.

**Formula:**  

\[
\text{Mean} = \frac{\text{Sum of all observations}}{\text{Number of observations}}
\]

---

### 🔹 Example

Marks of 5 students: `[70, 85, 90, 60, 95]`  

\[
\text{Mean} = \frac{70 + 85 + 90 + 60 + 95}{5} = \frac{400}{5} = 80
\]

**Interpretation:** The **average score** is 80.  

---

### 🔹 Key Points

- Sensitive to **outliers** (extremely high/low values)  
- Good for **numerical continuous data**  
- Often used in business & ML calculations  

---

# 2️⃣ Median

### 📌 Definition
The **median** is the **middle value** when data is arranged in ascending order.  

- If **odd number of values** → middle number  
- If **even number of values** → average of two middle numbers  

---

### 🔹 Example

Marks: `[70, 85, 90, 60, 95]`  

1. Arrange ascending: `[60, 70, 85, 90, 95]`  
2. Middle value → `85`  

**Interpretation:** Median score is 85  

---

### 🔹 Example with Even Numbers

Marks: `[60, 70, 85, 90]`  

1. Arrange ascending: `[60, 70, 85, 90]`  
2. Middle two: `70, 85`  
3. Median = `(70 + 85)/2 = 77.5`

---

### 🔹 Key Points

- **Not affected by outliers**  
- Good for **skewed data**  
- Represents the **central value** better than mean in skewed datasets  

---

# 3️⃣ Mode

### 📌 Definition
The **mode** is the value that **appears most frequently** in the dataset.

---

### 🔹 Example

Marks: `[70, 85, 90, 85, 95]`  

- Frequency of values:  
  - 70 → 1  
  - 85 → 2  
  - 90 → 1  
  - 95 → 1  

**Mode = 85** (appears twice)  

---

### 🔹 Key Points

- Can have **no mode, one mode, or multiple modes**  
- Useful for **categorical data**  
- Represents the **most popular value**  

---

# 4️⃣ When to Use Which Measure

| Measure | Best Use Case | Pros | Cons |
|---------|---------------|------|------|
| Mean    | Symmetric numerical data | Easy to calculate, widely used | Sensitive to outliers |
| Median  | Skewed numerical data | Not affected by outliers | Does not use all data |
| Mode    | Categorical or discrete data | Represents most common value | May not be unique |

---

# 5️⃣ Practical Example: Hospital Dataset

Suppose patient wait times (minutes) in ER:  
`[15, 20, 30, 15, 50, 15, 25]`  

### Step 1: Mean
\[
\text{Mean} = \frac{15+20+30+15+50+15+25}{7} = \frac{170}{7} \approx 24.3
\]

### Step 2: Median
Arrange ascending: `[15, 15, 15, 20, 25, 30, 50]`  
Middle value → `20`  

### Step 3: Mode
Most frequent → `15`  

**Interpretation:**  

- Average wait → 24.3 mins  
- Central value → 20 mins  
- Most common wait → 15 mins  

> Different measures provide **different insights**, all useful for decision-making.

---

# 6️⃣ Visual Representation

