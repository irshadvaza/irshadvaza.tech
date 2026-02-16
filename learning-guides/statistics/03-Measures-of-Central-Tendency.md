# 📘 Chapter 3 – Measures of Central Tendency

---

## 🎯 Why Measures of Central Tendency Matter

Measures of central tendency help us understand the **“center” or “typical” value** of a dataset.

- Simplifies large datasets  
- Summarizes data with a single representative value  
- Forms the basis for further analysis like variance, standard deviation, or probability  

**Example:**  
A teacher has marks of 5 students: `[70, 85, 90, 60, 95]`  
Instead of analyzing all numbers, we can use **mean, median, or mode** to understand the overall performance.

---

## 1️⃣ Mean (Average)

### 📌 Definition
The **mean** is the sum of all values divided by the total number of values.

**Formula:**  
Mean = (Sum of all observations) / (Number of observations)


### 🔹 Example (Manual Calculation)
Marks of 5 students: `[70, 85, 90, 60, 95]`  


Mean = (70 + 85 + 90 + 60 + 95) / 5 = 80



### 🔹 Python Example
```python
import numpy as np

# Data
data = [70, 85, 90, 60, 95]

# Mean
mean = np.mean(data)
print("Mean:", mean)'''




Mean: 80.0

'''

2️⃣ Median
📌 Definition

The median is the middle value when data is arranged in ascending order.

Odd number of values → middle number

Even number of values → average of two middle numbers

🔹 Example (Manual)

Marks: [70, 85, 90, 60, 95]

Arrange ascending: [60, 70, 85, 90, 95]

Middle value → 85

🔹 Python Example
import numpy as np

# Data
data = [70, 85, 90, 60, 95]

# Median
median = np.median(data)
print("Median:", median)


Output:
Median: 85.0

3️⃣ Mode
📌 Definition

The mode is the value that appears most frequently in the dataset.

🔹 Example (Manual)

Marks: [70, 85, 90, 85, 95]

Frequency of values:

70 → 1

85 → 2

90 → 1

95 → 1

Mode = 85 (appears twice)

🔹 Python Example
from scipy import stats

# Data
data = [70, 85, 90, 85, 95]

# Mode
mode = stats.mode(data)
print("Mode:", mode.mode[0])


Output:
Mode: 85

4️⃣ When to Use Which Measure
Measure	Best Use Case	Pros	Cons
Mean	Symmetric numerical data	Easy to calculate, widely used	Sensitive to outliers
Median	Skewed numerical data	Not affected by outliers	Does not use all data
Mode	Categorical or discrete data	Represents most common value	May not be unique
5️⃣ Practical Example: Hospital Dataset

Suppose patient wait times (minutes) in ER: [15, 20, 30, 15, 50, 15, 25]

🔹 Python Calculation
import numpy as np
from scipy import stats

# ER wait times
data = [15, 20, 30, 15, 50, 15, 25]

# Calculations
mean = np.mean(data)
median = np.median(data)
mode = stats.mode(data).mode[0]

print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)


Output:
Mean: 24.29
Median: 20.0
Mode: 15

Interpretation:

Average wait → 24.3 mins

Central value → 20 mins

Most common wait → 15 mins

Different measures provide different insights, all useful for decision-making.

6️⃣ Visual Representation
Data: 15, 15, 15, 20, 25, 30, 50

Mean      = 24.3 (average of all)
Median    = 20   (middle value)
Mode      = 15   (most frequent)


Graphically:

Frequency
3 |   ███
2 |
1 |           █
0 |_________________
   15 20 25 30 50

🔥 Tips & Tricks

Skewed data → Use median

Categorical data → Use mode

Clean numerical data → Use mean

Always check for outliers before choosing mean
