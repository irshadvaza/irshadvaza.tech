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



📦 Step 2 – Import Libraries & Load Dataset
Import Required Libraries

We first import all necessary Python libraries required for this project.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

Explanation

numpy → Used for numerical computations.

pandas → Used to load and manipulate structured data.

matplotlib & seaborn → Used for data visualization.

train_test_split → Splits dataset into training and testing sets.

StandardScaler → Scales numerical features (important for KNN because KNN is distance-based).

📥 Step 2.1 – Download and Load Dataset

We download the dataset using KaggleHub and load it into a pandas DataFrame.

import kagglehub

path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")

df = pd.read_csv(path + "/diabetes.csv")

Explanation

dataset_download() downloads the dataset from Kaggle.

pd.read_csv() reads the CSV file.

df now stores the full dataset.

📊 Step 2.2 – Explore the Dataset
1️⃣ Check Dataset Shape
df.shape


This shows:

Total number of rows

Total number of columns

Example output:

(768, 9)


Meaning:

768 records

9 columns

2️⃣ Check Data Types
df.dtypes


This shows the datatype of each column (int64, float64, etc.).

It helps verify:

All features are numeric

Dataset is suitable for KNN

3️⃣ View First 5 Rows
df.head()


This displays the first 5 rows of the dataset.

It helps to:

Understand feature values

Verify data loaded correctly

4️⃣ Check Class Distribution
df['Outcome'].value_counts()


This checks how many samples belong to each class.

Example output:

0    500
1    268


If one class has significantly more samples, the dataset is imbalanced.

5️⃣ Visualize Class Distribution
sns.countplot(x='Outcome', data=df)
plt.title("Class Distribution")
plt.show()


This creates a bar chart to visually inspect whether:

Class 0 (No Diabetes)

Class 1 (Diabetes)

are balanced or imbalanced.
