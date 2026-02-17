📘 Chapter 8 – Hypothesis Testing
📌 1️⃣ What is Hypothesis Testing?

Hypothesis Testing is a statistical method used to make decisions using data.

In simple words:

We test whether a claim about data is likely true or false.

It helps answer questions like:

Is a new medicine effective?

Did a new teaching method improve scores?

Is a marketing campaign increasing sales?

📌 2️⃣ Key Terminology

Before we go step-by-step, understand these basic terms.

🔹 Null Hypothesis (H₀)

Default assumption

Assumes no effect or no difference

Example:

H₀: The new teaching method has no effect on scores.

🔹 Alternative Hypothesis (H₁ or Ha)

Opposite of null hypothesis

Assumes there is an effect

Example:

H₁: The new teaching method improves scores.

📌 3️⃣ Step-by-Step Process of Hypothesis Testing
Step 1: State the Hypotheses
Step 2: Choose Significance Level (α)
Step 3: Select the Test
Step 4: Calculate Test Statistic
Step 5: Calculate p-value
Step 6: Make Decision


Let’s understand each step clearly.

📌 4️⃣ Step 1 – State the Hypotheses

Example Problem:

A company claims average salary is $50,000.

We want to test if it is different.

H₀: μ = 50000
H₁: μ ≠ 50000


This is a two-tailed test.

📌 5️⃣ Step 2 – Choose Significance Level (α)

Common values:

0.05 (most common)

0.01

0.10

If:

p-value < α


We reject the null hypothesis.

📌 6️⃣ Step 3 – Types of Tests
Test Type	When to Use
Z-Test	Large sample (n > 30)
T-Test	Small sample (n < 30)
Chi-Square Test	Categorical data
ANOVA	Compare 3+ groups

We will focus on T-Test (most common in Data Science).

📌 7️⃣ Example – One Sample T-Test
🎯 Problem

A school says average student score is 70.

We collect sample scores:

72, 75, 78, 74, 71, 69, 73


Test if average is different from 70.

Step 1 – Define Hypotheses
H₀: μ = 70
H₁: μ ≠ 70

Step 2 – Perform T-Test Using Python
import numpy as np
from scipy import stats

# Sample data
scores = [72, 75, 78, 74, 71, 69, 73]

# Perform one-sample t-test
t_stat, p_value = stats.ttest_1samp(scores, 70)

print("T-statistic:", t_stat)
print("P-value:", p_value)

Example Output
T-statistic: 2.97
P-value: 0.025

📌 8️⃣ Step 3 – Decision Making

If:

p-value < 0.05


Then:

✅ Reject H₀
❌ Reject claim that mean is 70

Since:

0.025 < 0.05


We reject the null hypothesis.

Conclusion:

The average score is significantly different from 70.

📌 9️⃣ Understanding p-value (Super Simple)

The p-value tells us:

How likely we would see this result if the null hypothesis were true.

Smaller p-value → stronger evidence against H₀

Quick Interpretation Guide
p-value	Meaning
> 0.05	Not significant
< 0.05	Significant
< 0.01	Very significant
📌 1️⃣0️⃣ Types of T-Tests
🔹 One Sample T-Test

Compare sample mean with known value.

🔹 Independent T-Test

Compare two independent groups.

Example:

Group A vs Group B

🔹 Paired T-Test

Compare before and after values.

Example:

Weight before diet vs after diet

📌 Example – Independent T-Test
from scipy import stats

group1 = [85, 88, 90, 86, 87]
group2 = [78, 80, 79, 81, 77]

t_stat, p_value = stats.ttest_ind(group1, group2)

print("T-statistic:", t_stat)
print("P-value:", p_value)


If p-value < 0.05 → groups are significantly different.

📌 1️⃣1️⃣ Type I and Type II Errors
🔹 Type I Error

Rejecting H₀ when it is actually true.

False positive.

Probability = α

🔹 Type II Error

Failing to reject H₀ when it is false.

False negative.

📌 1️⃣2️⃣ One-Tailed vs Two-Tailed Test
🔹 One-Tailed Test
H₁: μ > 70


OR

H₁: μ < 70


Used when direction matters.

🔹 Two-Tailed Test
H₁: μ ≠ 70


Used when checking for any difference.

📌 1️⃣3️⃣ Why Hypothesis Testing is Important in Data Science

Used in:

A/B Testing

Business decision making

Medical research

Machine Learning model comparison

Product testing

Marketing analysis

Every data-driven decision uses hypothesis testing.

🎯 Final Summary

Hypothesis Testing helps us:

Make decisions using data

Compare groups

Test claims

Validate assumptions

Key Concepts:

Null Hypothesis (H₀)

Alternative Hypothesis (H₁)

p-value

Significance level (α)

T-test

Errors (Type I & II)
