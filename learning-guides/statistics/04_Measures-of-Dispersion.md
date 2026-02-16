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



2️⃣ Variance
📌 Definition

Variance measures how far each value in the dataset is from the mean.

It is the average of squared differences from the mean

Higher variance → data more spread out

Formula:

Variance (σ²) = Σ (x_i - μ)² / N   # Population variance
Variance (s²) = Σ (x_i - x̄)² / (n-1)  # Sample variance

🔹 Example (Manual)

Data: [15, 20, 30, 15, 50, 15, 25]

Mean = 24.29

Differences from mean: [-9.29, -4.29, 5.71, -9.29, 25.71, -9.29, 0.71]

Squared differences: [86.3, 18.4, 32.6, 86.3, 660.5, 86.3, 0.5]

Variance (sample) = Sum / (n-1) = 970 / 6 ≈ 161.7

🔹 Python Example
import numpy as np

# Data
data = [15, 20, 30, 15, 50, 15, 25]

# Variance (sample)
variance = np.var(data, ddof=1)  # ddof=1 for sample variance
print("Variance:", variance)


Output:
Variance: 161.66666666666666

Interpretation:

Data is moderately spread out from the mean

Useful to understand consistency

3️⃣ Standard Deviation
📌 Definition

The standard deviation (SD) is the square root of variance.

Same unit as original data

Makes interpretation easier

Formula:

SD = √Variance

🔹 Example (Python)
import numpy as np

# Data
data = [15, 20, 30, 15, 50, 15, 25]

# Standard Deviation (sample)
std_dev = np.std(data, ddof=1)
print("Standard Deviation:", std_dev)


Output:
Standard Deviation: 12.715

Interpretation:

Most values are approximately ±12.7 minutes around the mean

Gives a clearer idea of spread than variance

4️⃣ Interquartile Range (IQR)
📌 Definition

IQR measures the spread of the middle 50% of data.

Q1 = 25th percentile

Q3 = 75th percentile

IQR = Q3 - Q1

Helps reduce effect of outliers

🔹 Example (Python)
import numpy as np

# Data
data = [15, 20, 30, 15, 50, 15, 25]

# Quartiles
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)

# IQR
IQR = Q3 - Q1
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)


Output:
Q1: 15.0
Q3: 30.0
IQR: 15.0

Interpretation:

The middle 50% of wait times vary by 15 minutes

Good measure when outliers exist

5️⃣ Comparison Table: Range vs Variance vs SD vs IQR
Measure	What it Tells	Pros	Cons
Range	Difference between max & min	Quick, simple	Sensitive to outliers
Variance	Average squared deviation	Uses all data	Units squared, hard to interpret
SD	Spread in original units	Easy to understand	Sensitive to outliers
IQR	Spread of middle 50%	Robust to outliers	Ignores some data
🔥 Practical Example: Hospital ER Wait Times

Data: [15, 20, 30, 15, 50, 15, 25]

import numpy as np
from scipy import stats

data = [15, 20, 30, 15, 50, 15, 25]

# Range
data_range = max(data) - min(data)

# Variance
variance = np.var(data, ddof=1)

# Standard Deviation
std_dev = np.std(data, ddof=1)

# IQR
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

print("Range:", data_range)
print("Variance:", variance)
print("Standard Deviation:", std_dev)
print("IQR:", IQR)


Output:
Range: 35
Variance: 161.6667
Standard Deviation: 12.715
IQR: 15

🏁 Summary

Range: Simple difference between max & min

Variance: Average squared distance from mean

Standard Deviation: Spread in original units

Interquartile Range: Spread of middle 50%, robust to outliers

Measures of dispersion complement mean, median, mode and give a complete picture of data distribution 🚀
