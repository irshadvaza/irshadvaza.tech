# 🧪 KNN Classification – Pima Indians Diabetes Dataset

## 📌 Objective

The objective of this lab is to build a Machine Learning classification model using **K-Nearest Neighbors (KNN)** to predict whether a patient has diabetes.

This project demonstrates:

- Data preprocessing
- Handling imbalanced dataset
- Feature scaling
- Hyperparameter tuning
- Model evaluation using multiple metrics
- Visualization of ROC and PR curves

---

## 📊 Dataset Description

We are using the **Pima Indians Diabetes Dataset**.

This dataset contains medical information about female patients of Pima Indian heritage.

### 🎯 Target Variable

| Value | Meaning |
|-------|---------|
| 0     | No Diabetes |
| 1     | Diabetes |

This is a **binary classification problem**.

---

## 📁 Features

| Feature | Description |
|----------|-------------|
| Pregnancies | Number of pregnancies |
| Glucose | Plasma glucose concentration |
| BloodPressure | Diastolic blood pressure |
| SkinThickness | Triceps skin fold thickness |
| Insulin | 2-Hour serum insulin |
| BMI | Body Mass Index |
| DiabetesPedigreeFunction | Genetic influence factor |
| Age | Age of patient |
| Outcome | Target variable |

---

## 🧠 Learning Goals

After completing this lab, you should understand:

- How KNN works
- Why scaling is important for distance-based models
- What is class imbalance
- How SMOTE helps balance data
- How GridSearch finds best hyperparameters
- How to evaluate classification models properly



# 📦 Step 2 – Import Libraries & Load Dataset

---

## 1️⃣ Import Required Libraries

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

🔎 Explanation:

numpy → For numerical calculations.

pandas → To load and manipulate tabular data.

matplotlib & seaborn → For plotting graphs and visualizations.

train_test_split → To split the dataset into training and testing sets.

StandardScaler → Scales numeric features so all features contribute equally to distance (important for KNN).


2️⃣ Download and Load Dataset
import kagglehub

# Download dataset
```
path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")
```

# Load CSV into DataFrame
```
df = pd.read_csv(path + "/diabetes.csv")
```

🔎 Explanation:

dataset_download() → Downloads dataset from Kaggle.

```
pd.read_csv() → Reads the CSV file into a pandas DataFrame.
```

df → Contains the full dataset including features and target column.

3️⃣ Explore the Dataset
a) Check Dataset Shape
```
df.shape
```

🔎 Explanation:

Returns the number of rows and columns.

Example output (768, 9) → 768 samples and 9 columns (including target).

b) Check Data Types
```
df.dtypes
```

🔎 Explanation:

Confirms the datatype of each column (int64, float64).

Ensures all features are numeric for KNN.

c) View First 5 Rows
```
df.head()
```

🔎 Explanation:

Displays the first 5 records of the dataset.

Helps verify data is loaded correctly and understand feature values.

d) Check Class Distribution
```
df['Outcome'].value_counts()
```

🔎 Explanation:

Counts samples in each class:

0 → No Diabetes

1 → Diabetes

Example output:

0    500
1    268


Indicates dataset is imbalanced because class 0 has almost twice the samples of class 1.

e) Visualize Class Distribution
```
sns.countplot(x='Outcome', data=df)
plt.title("Class Distribution")
plt.show()
```

🔎 Explanation:

Creates a bar chart showing number of samples in each class.

Helps visually confirm class imbalance.


# 📦 Step 3 – Data Cleaning & Preprocessing


## 1️⃣ Check Missing Values

```python
df.isnull().sum()
```

🔎 Explanation:

```
isnull().sum() checks for missing values in each column.
```

Missing values can cause errors in ML models.

In this dataset, there are no null values, but some medical features have zero values, which are unrealistic.

2️⃣ Identify Zero Values in Medical Fields

```
zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
(df[zero_cols] == 0).sum()
```

🔎 Explanation:

Some features like Glucose, BloodPressure, SkinThickness, Insulin, BMI should never be zero.

This code counts how many zero values exist in each of these columns.

3️⃣ Replace Zero Values with Median

```
for col in zero_cols:
    df[col] = df[col].replace(0, df[col].median())
```

🔎 Explanation:

Replaces all zeros in the selected columns with the median of that column.

Median is used instead of mean because it is less affected by outliers.

This cleans the dataset so all features have realistic values.

4️⃣ Check for Duplicates

```
df.duplicated().sum()
```

🔎 Explanation:

Checks if there are duplicate rows in the dataset.

Duplicate rows can bias the model.

5️⃣ Remove Duplicates

```
df = df.drop_duplicates()
```

🔎 Explanation:

Removes duplicate rows from the dataset.

Ensures each record is unique for better model training.

6️⃣ Define Features and Target

```
X = df.drop('Outcome', axis=1)

y = df['Outcome']
```

🔎 Explanation:

X → All features (input variables)

y → Target variable (Outcome: 0 or 1)

Prepares data for training/testing split.

7️⃣ Train-Test Split

```
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

```

🔎 Explanation:

Splits data into 80% training and 20% testing.

stratify=y → Ensures same class ratio in train and test sets.

random_state=42 → Ensures reproducibility.



Handling Imbalanced Data

The dataset has:

More non-diabetic patients

Fewer diabetic patients

This is called an Imbalanced Dataset.

Imbalanced datasets can bias the model toward the majority class.
We can handle this using SMOTE, Random Oversampling, or Random Undersampling.

1️⃣ SMOTE (Synthetic Minority Over-sampling Technique)

What is SMOTE?

Creates new artificial minority class samples.

Synthetic points are generated between real minority samples.

Balances dataset without duplicating data.

Example:

Before SMOTE:
Non-diabetic: 500
Diabetic    : 268

After SMOTE:
Non-diabetic: 500
Diabetic    : 500


Visual Idea:

Before: 0 0 0 0 1 1 1
After:  0 0 0 0 1 1 1 1 1 1  <- synthetic 1s added


Python Code:

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X_train, y_train)

print("After SMOTE:", y_res.value_counts())


✅ Key Points:

Creates new synthetic samples

Works well for small datasets

Balances classes efficiently

2️⃣ Random Oversampling

What is Random Oversampling?

Randomly duplicates minority samples until classes are balanced.

Does not create new data, only copies existing rows.

Example:

Before:
Non-diabetic: 500
Diabetic    : 200

After Random Oversampling:
Non-diabetic: 500
Diabetic    : 500


Visual Idea:

Before: 0 0 0 0 1 1
After:  0 0 0 0 1 1 1 1 1  <- duplicates added


Python Code:

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X_train, y_train)

print("After Oversampling:", y_res.value_counts())


✅ Key Points:

Simple to implement

Maintains all majority data

Risk: Overfitting due to duplicated data

3️⃣ Random Undersampling

What is Random Undersampling?

Randomly removes samples from majority class to balance dataset.

Reduces the size of the majority class instead of increasing minority.

Example:

Before:
Non-diabetic: 500
Diabetic    : 200

After Random Undersampling:
Non-diabetic: 200
Diabetic    : 200


Visual Idea:

Before: 0 0 0 0 0 1 1
After:  0 0 1 1 <- some majority 0s removed


Python Code:

from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(X_train, y_train)

print("After Undersampling:", y_res.value_counts())


✅ Key Points:

Fast and memory-efficient

May discard useful majority data

Good for very large datasets

4️⃣ Comparison Table
Method	How it Works	New Data?	Pros	Cons
SMOTE	Generates synthetic minority samples	✅ Yes	Balances dataset without duplication	Slight noise possible
Random Oversampling	Duplicates minority samples	❌ No	Simple, keeps all majority	Overfitting risk
Random Undersampling	Removes majority samples	❌ No	Fast, reduces dataset size	Data loss, less info
5️⃣ Tips / Recommendations

SMOTE → Use for small/medium datasets, especially medical datasets.

Random Oversampling → Simple solution when dataset is small.

Random Undersampling → Use for very large datasets or memory issues.

✅ Visual Summary (Quick Diagram)

Dataset: 0=majority, 1=minority

Original:        0 0 0 0 1 1
SMOTE:           0 0 0 0 1 1 1 1
Random Oversample:0 0 0 0 1 1 1 1
Random Undersample:0 0 1 1

