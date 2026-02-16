# 📘 Chapter 4 – Measures of Dispersion

---

## 🎯 Why Measures of Dispersion Matter

Measures of dispersion tell us **how spread out or varied** the data is.  

- Mean tells the center, but **dispersion tells how data spreads around the mean**  
- Helps understand **consistency** of data  
- Useful for **risk analysis, quality control, and decision-making**

---

## 1️⃣ Range

### 📌 Definition
The **range** is the difference between the **maximum** and **minimum** values in a dataset.

**Formula:**  
Range = Maximum value - Minimum value


### 🔹 Example (Manual)
Patient wait times (minutes): `[15, 20, 30, 15, 50, 15, 25]`  

- Maximum = 50  
- Minimum = 15  
- Range = 50 - 15 = 35 minutes

### 🔹 Python Example
```python
# Data
data = [15, 20, 30, 15, 50, 15, 25]

# Range
data_range = max(data) - min(data)
print("Range:", data_range)


Output:
Range: 35

Interpretation:

The wait times vary by 35 minutes

Gives a quick idea of variability, but doesn’t show how values are distributed
