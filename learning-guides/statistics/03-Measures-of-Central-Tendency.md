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
print("Mean:", mean)

**Output**
