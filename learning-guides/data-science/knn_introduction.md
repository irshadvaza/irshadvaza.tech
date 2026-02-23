# 👶 K-Nearest Neighbors (KNN) – Explained from Scratch

KNN is one of the **simplest machine learning algorithms**.  
We’ll explain it in a **super simple way**, step by step, for someone who has **never seen ML before**.

---

## Step 1: Imagine a Playground

Imagine a **playground** where kids are either:

- 🏀 **Basketball players** (label = 1)  
- ⚽ **Soccer players** (label = 0)

We have a **new kid** who arrives and we want to know:

> “Which sport will the new kid like?”  

---

## Step 2: Look at the Neighbors

We decide to **ask the closest kids** around the new kid.  

- K = 3 → Look at 3 nearest kids  
- K = 5 → Look at 5 nearest kids  

> This is exactly why it’s called **K-Nearest Neighbors**.

---

## Step 3: Count the Votes

Example:

| Neighbor | Sport |
|----------|-------|
| 1        | Basketball 🏀 |
| 2        | Basketball 🏀 |
| 3        | Soccer ⚽ |

- **Count votes**:  
  - Basketball = 2  
  - Soccer = 1  

✅ Prediction: **Basketball** (majority vote wins)  

> KNN **just looks at neighbors and takes a majority vote**.

---

## Step 4: How Do We Measure "Close"?

We need a way to **measure distance**.  

Imagine each kid is standing at a point on the playground:

- **Distance formula** tells us how far they are:  
  - Euclidean distance = “straight line”  
  - Manhattan distance = “grid lines like a city map”

> KNN uses distance to find the **closest K neighbors**.

---

## Step 5: Features Matter

Each kid can have features like:

- Height  
- Age  
- Weight  

Distance is calculated based on these numbers.  

> Problem: If height = 150 and weight = 30, height dominates distance.  
> **Solution:** Scale all features (StandardScaler).

---

## Step 6: Python Example

Imagine we have a small dataset of kids:

```python
# Features: [height, weight]
X = [[150, 30], [160, 35], [170, 60], [155, 33], [180, 70]]
# Labels: 1 = Basketball, 0 = Soccer
y = [1, 1, 0, 1, 0]

from sklearn.neighbors import KNeighborsClassifier

# Create KNN with K=3
knn = KNeighborsClassifier(n_neighbors=3)

# Train the model
knn.fit(X, y)

# New kid: height=165, weight=40
new_kid = [[165, 40]]
prediction = knn.predict(new_kid)

print("Predicted Sport:", "Basketball 🏀" if prediction[0]==1 else "Soccer ⚽")
```

## Step 7: Key Points

KNN does not train in the usual way. It remembers the dataset.

Prediction = look at K closest neighbors → take majority vote

Distance can be Euclidean or Manhattan

Scaling is important if features have different ranges

## Step 8: Choosing K

Small K → sensitive to noise → may overfit

Large K → smoother predictions → may underfit

Best K is usually found using GridSearchCV.

## ✅ Summary for Beginners

Imagine new data points in a playground

Look at the nearest neighbors

Count the votes

Predict based on majority

That’s KNN in the simplest terms!




## Step 2: What Are Hyperparameters?

Hyperparameters are like knobs or settings for the model.

For KNN, we can adjust 3 important knobs:

1️⃣ n_neighbors → How many neighbors to look at
2️⃣ weights → Do all neighbors count equally? Or do closer neighbors count more?
3️⃣ metric → How do we measure distance between points?

Step 3: Set Hyperparameter Options
param_grid = {
    'n_neighbors': [3,5,7,9,11],
    'weights': ['uniform','distance'],
    'metric': ['euclidean','manhattan']
}

1️⃣ n_neighbors (K)

n_neighbors = [3,5,7,9,11]

This means we want the model to try K=3, K=5, K=7, K=9, K=11

Example:

If K = 3 → looks at 3 nearest patients

If K = 5 → looks at 5 nearest patients

Effect:

K	Effect
Small (3)	Sensitive to nearby points, may overfit
Large (11)	Looks at many points, may underfit, smoother prediction
2️⃣ weights

'uniform' → All neighbors have equal importance

'distance' → Closer neighbors have more importance

Example:

K = 3 neighbors:

Neighbors: [closest, middle, farthest]

Uniform: each neighbor counts 1 vote

Distance: closest neighbor counts more than the farthest

Usually, 'distance' gives better results because the nearest points are more relevant.

3️⃣ metric

How do we measure distance between patients?

Options:

Metric	Description
'euclidean'	Straight line distance
'manhattan'	Grid-like distance (like city blocks)

Example:

Patient A: Glucose=150, BMI=30

Patient B: Glucose=160, BMI=32

Euclidean: straight line between points

Manhattan: sum of horizontal + vertical differences

KNN uses this to find the closest neighbors.

Step 4: Why We Try Many Combinations

We don’t know which combination is best:

Small K or Large K?

Uniform or Distance?

Euclidean or Manhattan?

So we try all combinations using GridSearchCV (covered in the next step).
