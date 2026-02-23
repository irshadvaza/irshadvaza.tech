K-Nearest Neighbors (KNN)
📘 What is KNN?

KNN = K-Nearest Neighbors

One of the simplest machine learning algorithms.

Works based on distance between data points.

Predicts the class of a new point by looking at its K closest neighbors.

🧠 Simple Real-Life Example

Imagine:

You move to a new city and want to know if a neighborhood is safe.

You ask your 5 nearest neighbors.

If:

4 say it is safe

1 says it is not safe

You decide → It is safe ✅

This is exactly how KNN works: it looks at nearby points and predicts based on the majority vote.

🎯 KNN in Our Diabetes Problem

We want to predict:

👉 Does a patient have diabetes or not?

Steps KNN follows:

Take a new patient.

Measure distance to all other patients.

Select K closest patients.

Check the majority class among neighbors.

Predict based on majority vote.

🔢 What is K?

K = number of neighbors considered for prediction.

Example:

If K = 3, look at 3 closest patients:

2 diabetic

1 non-diabetic

Prediction = Diabetic ✅

📏 How Distance is Measured?

Euclidean distance → straight-line distance

Manhattan distance → grid-based distance

💡 Why Scaling is Important?

If one feature is much larger than others, e.g.:

Glucose = 150

BMI = 30

Then distance is dominated by the larger feature → misleading results

Solution: Use StandardScaler to normalize all features.

📦 Advantages of KNN

✔ Simple to understand
✔ Easy to implement
✔ No training time (lazy learner)

⚠ Disadvantages of KNN

❌ Slow for large datasets
❌ Sensitive to feature scaling
❌ Sensitive to irrelevant features

🔹 Example (Diabetes KNN)

If K = 5:

Checks 5 closest points

Majority vote decides the class

Example:

3 diabetic

2 non-diabetic

Prediction = Diabetic ✅
