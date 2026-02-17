📘 Chapter 6 – Random Variables
📌 1️⃣ What is a Random Variable?

A Random Variable is a variable whose value depends on the outcome of a random experiment.

👉 In simple words:

A random variable assigns a numerical value to each possible outcome of an experiment.

🎯 Example 1 – Tossing a Coin

Experiment: Toss a coin once.

Possible outcomes:

Head (H)

Tail (T)

Now define a random variable X:

X = 1 if Head  
X = 0 if Tail


So:

Outcome	X (Value)
Head	1
Tail	0

Here, X is a Random Variable.

📌 2️⃣ Types of Random Variables

There are 2 main types:

Random Variable
│
├── Discrete Random Variable
│
└── Continuous Random Variable

📌 3️⃣ Discrete Random Variable

A Discrete Random Variable takes countable values.

Usually integers.

🎯 Example – Rolling a Dice

Experiment: Roll a fair dice.

Possible values:

1, 2, 3, 4, 5, 6


If we define:

X = Number showing on dice


Then X is a Discrete Random Variable.

📊 Probability Distribution (Discrete)

For a fair dice:

X	Probability P(X)
1	1/6
2	1/6
3	1/6
4	1/6
5	1/6
6	1/6
🐍 Python Example – Discrete Random Variable
import numpy as np

# Simulate rolling a dice 10 times
dice_rolls = np.random.randint(1, 7, 10)

print("Dice Rolls:", dice_rolls)


Output (example):

Dice Rolls: [3 1 6 2 4 5 2 6 1 3]


Each roll is a discrete random value.

📌 4️⃣ Continuous Random Variable

A Continuous Random Variable takes infinite values within a range.

These are measured values.

🎯 Example – Height of Students

Height can be:

170.1 cm
170.12 cm
170.123 cm


Infinite possibilities.

So height is a Continuous Random Variable.

🎯 Example – Temperature

Temperature can be:

25°C
25.5°C
25.52°C


Infinite precision → Continuous.

🐍 Python Example – Continuous Random Variable
import numpy as np

# Generate 5 random heights (normal distribution)
heights = np.random.normal(loc=170, scale=5, size=5)

print("Sample Heights:", heights)


Output (example):

Sample Heights: [168.4 171.2 173.5 169.8 172.1]


These are continuous values.

📌 5️⃣ Probability of a Random Variable

For Discrete Random Variable:

We calculate:

P(X = x)


For Continuous Random Variable:

We calculate probability over a range:

P(a < X < b)


Because probability at exact single point is zero.

📌 6️⃣ Expected Value (Mean of Random Variable)

The Expected Value tells us the long-term average.

🎯 Example – Dice Expected Value

For a fair dice:

𝐸
(
𝑋
)
=
(
1
×
1
/
6
)
+
(
2
×
1
/
6
)
+
.
.
.
+
(
6
×
1
/
6
)
E(X)=(1×1/6)+(2×1/6)+...+(6×1/6)
𝐸
(
𝑋
)
=
3.5
E(X)=3.5
🐍 Python Example – Expected Value
import numpy as np

# Dice values
values = np.array([1, 2, 3, 4, 5, 6])
probabilities = np.array([1/6] * 6)

expected_value = np.sum(values * probabilities)

print("Expected Value:", expected_value)


Output:

Expected Value: 3.5

📌 7️⃣ Variance of Random Variable

Variance measures spread around expected value.

Formula:

𝑉
𝑎
𝑟
(
𝑋
)
=
𝐸
[
(
𝑋
−
𝜇
)
2
]
Var(X)=E[(X−μ)
2
]
🐍 Python Example – Variance of Dice
import numpy as np

values = np.array([1, 2, 3, 4, 5, 6])
probabilities = np.array([1/6] * 6)

mean = np.sum(values * probabilities)

variance = np.sum(probabilities * (values - mean)**2)

print("Variance:", variance)


Output:

Variance: 2.9167

📌 8️⃣ Discrete vs Continuous (Quick Comparison)
Feature	Discrete	Continuous
Values	Countable	Infinite
Example	Dice roll	Height
Graph	Bar chart	Smooth curve
Probability	P(X = x)	P(a < X < b)
📌 9️⃣ Real Data Science Applications

Random variables are used in:

Machine Learning models

Risk analysis

Forecasting

A/B Testing

Predictive modeling

Financial modeling

AI algorithms

Every ML model is based on probability and random variables.

🎯 Final Summary

A Random Variable:

Converts outcomes into numbers

Can be Discrete or Continuous

Has probability distribution

Has expected value (mean)

Has variance (spread)
