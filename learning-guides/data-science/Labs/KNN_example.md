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



# 📦 Step 2 – Import Required Libraries

We first import all required Python libraries.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


📥 Step 2.1 – Download and Load Dataset

We download the dataset using KaggleHub.

import kagglehub

path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")

df = pd.read_csv(path + "/diabetes.csv")

🔎 Explanation

dataset_download() downloads dataset.

pd.read_csv() loads the CSV file into a pandas DataFrame.

df now contains our dataset.

📊 Step 2.2 – Explore the Dataset
Shape of Dataset
df.shape


Shows:

Number of rows

Number of columns

