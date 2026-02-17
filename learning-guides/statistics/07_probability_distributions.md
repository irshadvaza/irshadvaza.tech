📘 Chapter 7 – Probability Distributions
📌 1️⃣ What is a Probability Distribution?

A Probability Distribution shows:

How probabilities are distributed across possible values of a Random Variable.

In simple words:

It tells us:

What values can occur

How likely each value is


📌 2️⃣ Two Types of Probability Distributions

Probability Distribution
│
├── Discrete Probability Distribution
│
└── Continuous Probability Distribution

📌 3️⃣ Discrete Probability Distributions

Used when random variable is countable.

Examples:

Number of heads

Number of customers

Number of defects

🎯 Example 1 – Dice Distribution

If you roll a fair dice:

Value (X)	Probability P(X)

1	1/6
2	1/6
3	1/6
4	1/6
5	1/6
6	1/6

This table is a Probability Distribution.

📌 4️⃣ Important Discrete Distributions

We will study:

Binomial Distribution

Poisson Distribution

🎯 4.1 Binomial Distribution

Used when:

Fixed number of trials (n)

Only 2 outcomes (Success / Failure)

Same probability of success (p)

🎯 Example – Toss Coin 3 Times

Let:

n = 3

p = 0.5

X = Number of Heads

Possible values:

0, 1, 2, 3

🧮 Binomial Formula
𝑃(𝑋=𝑘)=(𝑛𝑘)𝑝𝑘(1−𝑝)𝑛
−
𝑘
P(X=k)=(
k
n
	​

)p
k
(1−p)
n−k

Where:

n = number of trials

k = number of successes

p = probability of success

🐍 Python Example – Binomial Distribution
from scipy.stats import binom

# n = 3 trials, p = 0.5 probability of head
n = 3
p = 0.5

# Probability of getting exactly 2 heads
prob = binom.pmf(2, n, p)

print("Probability of 2 Heads:", prob)


Output:

Probability of 2 Heads: 0.375

🎯 4.2 Poisson Distribution

Used when:

Counting events

Events occur in fixed interval

Events are independent

Examples:

Number of calls per hour

Number of defects per machine

Number of website visits per minute

🧮 Poisson Formula
𝑃
(
𝑋
=
𝑘
)
=
𝑒
−
𝜆
𝜆
𝑘
𝑘
!
P(X=k)=
k!
e
−λ
λ
k
	​


Where:

λ (lambda) = average number of events

🎯 Example – Customer Calls

If average calls per hour = 4

What is probability of getting exactly 2 calls?

🐍 Python Example – Poisson Distribution
from scipy.stats import poisson

# lambda = 4
lam = 4

# Probability of 2 calls
prob = poisson.pmf(2, lam)

print("Probability of 2 calls:", prob)


Output:

Probability of 2 calls: 0.1465

📌 5️⃣ Continuous Probability Distributions

Used when values are measurable and infinite.

Examples:

Height

Weight

Temperature

Salary

📌 6️⃣ Important Continuous Distributions

We will study:

Normal Distribution

Uniform Distribution

🎯 6.1 Normal Distribution (Most Important)

Also called:

Bell Curve

It is:

Symmetrical

Mean = Median = Mode

Used everywhere in Data Science

🎯 Real Examples

Student marks

Human height

Measurement errors

Stock returns

📊 Properties

Bell shaped

Centered at mean (μ)

Spread controlled by standard deviation (σ)

🐍 Python Example – Normal Distribution
import numpy as np

# Generate 5 values from normal distribution
data = np.random.normal(loc=50, scale=10, size=5)

print("Random Values:", data)


Output (example):

Random Values: [52.3 47.8 61.2 49.5 44.1]

🎯 6.2 Uniform Distribution

In Uniform Distribution:

Every value has equal probability.

Example:

Random number between 0 and 1

Random lottery number

🐍 Python Example – Uniform Distribution
import numpy as np

# Generate 5 uniform values between 0 and 1
data = np.random.uniform(0, 1, 5)

print("Uniform Values:", data)


Output (example):

Uniform Values: [0.21 0.78 0.45 0.11 0.67]

📌 7️⃣ Discrete vs Continuous Summary
Feature	Discrete	Continuous
Values	Countable	Infinite
Example	Dice	Height
Graph	Bars	Curve
Exact Probability	Yes	No
Range Probability	Yes	Yes
📌 8️⃣ Why Probability Distributions Matter in Data Science?

Used in:

Machine Learning

Risk modeling

Fraud detection

A/B Testing

Forecasting

Financial modeling

AI algorithms

Almost every ML algorithm assumes some distribution.

🎯 Final Summary

A Probability Distribution:

Shows likelihood of outcomes

Can be Discrete or Continuous

Includes:

Binomial

Poisson

Normal

Uniform

Forms foundation of Machine Learning
