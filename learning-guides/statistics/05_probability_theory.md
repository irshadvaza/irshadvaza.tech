📘 Chapter 5 – Probability Theory

(Step-by-step, beginner-friendly, with Python examples and clean formatting)

You can copy-paste this directly.

# 📘 Chapter 5 – Probability Theory

---

## 🎯 Why Probability Matters

Probability helps us measure **uncertainty**.

- What is the chance of rain tomorrow?
- What is the probability of getting heads in a coin toss?
- What is the likelihood a customer buys a product?

Probability is the **foundation of statistics, machine learning, and AI**.

---

# 1️⃣ Basic Concepts of Probability

## 📌 Definition

Probability measures how likely an event is to occur.



Probability = (Number of favorable outcomes) / (Total number of possible outcomes)


The value of probability is always between:



0 ≤ P(Event) ≤ 1


- 0 → Impossible event  
- 1 → Certain event  

---

## 🔹 Example 1: Tossing a Coin

Possible outcomes:



Sample Space = {Heads, Tails}


What is the probability of getting Heads?



P(Heads) = 1 / 2 = 0.5


---

## 🔹 Python Example

```python
# Probability of getting heads in a fair coin

favorable_outcomes = 1
total_outcomes = 2

probability = favorable_outcomes / total_outcomes
print("Probability of Heads:", probability)


Output:
Probability of Heads: 0.5

2️⃣ Sample Space & Events
📌 Sample Space (S)

The set of all possible outcomes.

Example: Rolling a dice

S = {1, 2, 3, 4, 5, 6}

📌 Event (E)

An event is a subset of the sample space.

Example: Getting an even number

E = {2, 4, 6}

🔹 Example: Dice Roll

What is the probability of getting an even number?

P(Even) = 3 / 6 = 0.5

🔹 Python Example
# Dice example

sample_space = [1, 2, 3, 4, 5, 6]
even_numbers = [2, 4, 6]

probability_even = len(even_numbers) / len(sample_space)
print("Probability of Even Number:", probability_even)


Output:
Probability of Even Number: 0.5

3️⃣ Types of Probability
📌 1. Theoretical Probability

Based on mathematical reasoning.

Example:

P(Heads) = 1/2

📌 2. Experimental Probability

Based on actual experiments.

Example:
If we toss a coin 10 times and get 6 heads:

Experimental Probability = 6 / 10 = 0.6

🔹 Python Simulation Example
import random

# Simulate 10 coin tosses
tosses = 10
heads = 0

for _ in range(tosses):
    if random.choice(["H", "T"]) == "H":
        heads += 1

experimental_probability = heads / tosses
print("Experimental Probability of Heads:", experimental_probability)


Output Example:
Experimental Probability of Heads: 0.6
(Output may vary because it's random.)

4️⃣ Conditional Probability
📌 Definition

Conditional probability is the probability of an event occurring given that another event has already occurred.

P(A | B) = P(A and B) / P(B)

🔹 Example

In a class:

60% are boys

30% are boys who play cricket

What is the probability that a student plays cricket given that the student is a boy?

P(Cricket | Boy) = 0.30 / 0.60 = 0.5

🔹 Python Example
P_boy = 0.60
P_boy_and_cricket = 0.30

conditional_probability = P_boy_and_cricket / P_boy
print("P(Cricket | Boy):", conditional_probability)


Output:
P(Cricket | Boy): 0.5

5️⃣ Independent vs Dependent Events
📌 Independent Events

One event does NOT affect the other.

Example:
Two coin tosses.

P(A and B) = P(A) × P(B)


Example:

P(Heads twice) = 1/2 × 1/2 = 1/4

🔹 Python Example
P_head = 0.5

P_two_heads = P_head * P_head
print("Probability of Two Heads:", P_two_heads)


Output:
Probability of Two Heads: 0.25

6️⃣ Complement Rule

The probability that an event does NOT happen.

P(Not A) = 1 - P(A)


Example:
If probability of rain = 0.3

P(No Rain) = 1 - 0.3 = 0.7

🔹 Python Example
P_rain = 0.3
P_no_rain = 1 - P_rain

print("Probability of No Rain:", P_no_rain)


Output:
Probability of No Rain: 0.7

📊 Summary Table
Concept	Formula	Key Idea
Basic Probability	Favorable / Total	Likelihood of event
Conditional	P(A and B) / P(B)	Given another event
Independent	P(A) × P(B)	Events don't affect each other
Complement	1 - P(A)	Opposite event
🏁 Final Summary

Probability measures uncertainty

Always between 0 and 1

Sample space = all outcomes

Conditional probability handles dependent situations

Independent events multiply probabilities

Probability is the backbone of machine learning models like Naive Bayes, Bayesian inference, and decision theory 🚀
