# 🏥 K-Nearest Neighbors (KNN)

KNN is a **simple machine learning algorithm** used for classification.  
It predicts the **class of a new data point** based on the **K closest neighbors** in the dataset.  

---

## 📘 What is KNN?

- **Full Name:** K-Nearest Neighbors  
- **Type:** Lazy learner, instance-based algorithm  
- **Idea:** Similar points belong to the same class  
- **Prediction:** Based on the **majority vote** of K nearest neighbors  

> KNN **does not train a model**; it stores the dataset and predicts based on neighbors.

---

## 🧠 Real-Life Analogy

Imagine moving to a new city and asking your **5 nearest neighbors** if the neighborhood is safe:  

- ✅ 4 say safe  
- ❌ 1 says unsafe  

You conclude → **Safe**  

> KNN works the same way using **majority vote** from the closest points.

---

## 🎯 KNN in Diabetes Prediction

We want to predict **whether a patient has diabetes**.  

**Steps KNN follows:**

1. Take a **new patient**  
2. Measure **distance** to all other patients  
3. Select **K closest patients**  
4. Check **majority class**  
5. Predict patient’s class  

---

## 🔢 Understanding K

- K = number of neighbors considered for prediction  

**Example:**

| K | Neighbors | Class Distribution | Prediction |
|---|-----------|-----------------|------------|
| 3 | 2 diabetic, 1 non-diabetic | Majority = Diabetic | ✅ Diabetic |
| 5 | 3 non-diabetic, 2 diabetic | Majority = Non-diabetic | ❌ Non-diabetic |

> Choosing K is important:  
> - Small K → sensitive to noise (may overfit)  
> - Large K → smoother predictions (may underfit)

---

## 📏 Distance Metrics

| Metric | Description | Formula |
|--------|-------------|---------|
| Euclidean | Straight-line distance | √((x1-x2)² + (y1-y2)²) |
| Manhattan | Grid-like distance | |x1-x2| + |y1-y2| |

---

## 💡 Why Feature Scaling is Important

Example:

- Glucose = 150  
- BMI = 30  

Without scaling, **Glucose dominates distance**, misleading results.  

**Solution:** Use **StandardScaler** to normalize all features.

---

## 📦 Advantages of KNN

- ✅ Simple and intuitive  
- ✅ Easy to implement  
- ✅ No training time (lazy learner)  

---

## ⚠ Disadvantages of KNN

- ❌ Slow for large datasets  
- ❌ Sensitive to feature scaling  
- ❌ Sensitive to irrelevant features  

---

## 🔹 Example – Diabetes Dataset

If K = 5:

- Checks **5 nearest points**  
- Majority vote decides class  

```text
Neighbors: 1 1 0 1 0
Class Labels: Diabetic=1, Non-diabetic=0
Majority = 1 → Predict Diabetic ✅
```


```
from sklearn.neighbors import KNeighborsClassifier

# Create KNN model
model = KNeighborsClassifier()

# Hyperparameter grid
param_grid = {
    'n_neighbors': [3,5,7,9,11],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}
```

Explanation:

n_neighbors → number of neighbors to consider

weights → 'uniform' (all neighbors equal) or 'distance' (closer neighbors weigh more)

metric → distance calculation method

📊 Visual Intuition

```
Original Dataset: 0 0 0 1 1
New Point:        ?
Neighbors: 1 1 0 1 0
Majority = 1 → Predict Diabetic ✅
```

```
🔹 Detailed GridSearchCV Hyperparameters

1️⃣ n_neighbors

'n_neighbors': [3,5,7,9,11]
```

Try different K values:
• 3 neighbors
• 5 neighbors
• 7 neighbors
• 9 neighbors
• 11 neighbors

Why?
Because we don’t know which K gives the best performance.

Small K:
• More sensitive
• May overfit

Large K:
• More stable
• May underfit

So we test multiple values to find the optimal K.

2️⃣ weights

'weights': ['uniform', 'distance']


uniform: All neighbors have equal importance.

Example: If K=5, each neighbor has same vote.

distance: Closer neighbors have more importance.

Example: The nearest patient influences prediction more.

Usually performs better than uniform weighting.

3️⃣ metric

'metric': ['euclidean', 'manhattan']


Defines how distance is calculated between points.

Euclidean: straight-line distance

Manhattan: grid-based distance
'''

```
3️⃣ GridSearchCV with RepeatedStratifiedKFold

We are doing two things:

1️⃣ Cross-validation → RepeatedStratifiedKFold
2️⃣ Hyperparameter tuning → GridSearchCV

🔹 Importing the Tools
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold


GridSearchCV: Finds the best parameter combination

RepeatedStratifiedKFold: Performs robust cross-validation

🔹 Setting up Cross-Validation
cv = RepeatedStratifiedKFold(
    n_splits=5,
    n_repeats=3,
    random_state=42
)


K-Fold: Dataset split into 5 parts → each used once as validation

Stratified: Each fold maintains class ratio (important for imbalanced datasets)

Repeated: 5-fold process repeated 3 times → more reliable results

🔹 GridSearchCV
grid = GridSearchCV(
    model,
    param_grid,
    cv=cv,
    scoring='roc_auc',
    n_jobs=-1
)


Tries all combinations in param_grid

Uses cross-validation to evaluate each combination

Selects the best parameters

🔹 Hyperparameters Explained
1️⃣ n_neighbors

[3,5,7,9,11] → Try different K values

Small K → sensitive, may overfit

Large K → stable, may underfit

2️⃣ weights

'uniform' → all neighbors equal

'distance' → closer neighbors weigh more (usually better)

3️⃣ metric

'euclidean' → straight-line distance

'manhattan' → grid-like distance

🔹 Fitting GridSearch
grid.fit(X_train_res, y_train_res)

print("Best Parameters:", grid.best_params_)
print("Best CV Score:", grid.best_score_)


Example Output:

Best Parameters: {'n_neighbors': 5, 'weights': 'distance', 'metric': 'euclidean'}
Best CV Score: 0.83

✅ Summary

RepeatedStratifiedKFold → robust, stratified cross-validation

GridSearchCV → systematic hyperparameter tuning

Together: finds best KNN parameters with reliable performance
