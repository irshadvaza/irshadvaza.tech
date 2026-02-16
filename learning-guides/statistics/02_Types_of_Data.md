📘 Chapter 2 – Types of Data
🎯 Why Understanding Types of Data is Important

Before calculating mean, probability, regression, or building machine learning models, we must answer one simple question:

What kind of data are we working with?

Because:

The type of data determines which statistical method to use.

Wrong method → Wrong conclusion.

Correct classification → Correct analysis.

📌 Example:

You can calculate average salary ✅

You cannot calculate average gender ❌

Understanding data types is the foundation of statistics and data science.

🧠 Step 1: Broad Classification of Data

In statistics, data is divided into two main categories:

1️⃣ Qualitative Data (Categorical Data)
2️⃣ Quantitative Data (Numerical Data)


Let’s understand them step by step.

1️⃣ Qualitative Data (Categorical Data)
📌 Simple Meaning

Qualitative data describes qualities, labels, or categories.

It answers:

What type?

Which category?

What group?

It does NOT represent numbers that we can calculate mathematically.

🔹 Example
Student Name	Gender	Blood Group
Aisha	Female	O+
Rahul	Male	B+

Here:

Gender → Categorical

Blood Group → Categorical

We cannot calculate:

Average of Male and Female ❌
Average of Blood Group ❌

🔹 Types of Qualitative Data

Qualitative data has two subtypes:

A) Nominal Data
📌 Meaning

Categories with no specific order.

There is no ranking or hierarchy.

📌 Examples

Gender (Male, Female)

Blood Group (A, B, AB, O)

City Names

Religion

Department Names

You cannot say:

A is greater than B ❌

Male is higher than Female ❌

Nominal = Just names or labels.

B) Ordinal Data
📌 Meaning

Categories that have a meaningful order or ranking.

There is a sequence, but the difference between levels is not measurable.

📌 Examples

Education Level (School < College < University)

Customer Rating (1 ⭐ < 2 ⭐ < 3 ⭐ < 4 ⭐ < 5 ⭐)

Satisfaction Level (Low < Medium < High)

Severity Level (Mild < Moderate < Severe)

Here, ranking exists.

But:

Difference between 1-star and 2-star is not mathematically measurable.

We cannot assume equal distance between categories.

Ordinal = Order exists, but numeric calculation is limited.

2️⃣ Quantitative Data (Numerical Data)
📌 Simple Meaning

Quantitative data represents numbers that can be measured and calculated.

You can perform:

Addition

Subtraction

Multiplication

Division

Mean

Variance

Standard deviation

🔹 Example
Employee	Salary	Age
John	50,000	30
Meera	60,000	35

Here:

Salary → Quantitative

Age → Quantitative

We can calculate:

Average salary ✅

Average age ✅

Variance of salary ✅

🔹 Types of Quantitative Data

Quantitative data also has two subtypes:

A) Discrete Data
📌 Meaning

Data that can be counted.

Usually whole numbers.

📌 Examples

Number of students in a class

Number of cars in parking

Number of hospital patients

Number of calls received

You cannot have:

3.5 students ❌

7.2 patients ❌

Discrete data comes from counting.

B) Continuous Data
📌 Meaning

Data that can be measured and can take any value within a range.

It can include decimals.

📌 Examples

Height (170.5 cm)

Weight (65.8 kg)

Temperature (36.7°C)

Time (5.23 seconds)

Blood Pressure (120.7 mmHg)

You can have:

65.75 kg ✅

98.456 seconds ✅

Continuous data comes from measurement.

📊 Visual Summary
Data
│
├── Qualitative (Categorical)
│     ├── Nominal (No order)
│     └── Ordinal (With order)
│
└── Quantitative (Numerical)
      ├── Discrete (Countable)
      └── Continuous (Measurable)

🏥 Real-Life Example (Hospital Dataset)

Imagine hospital data:

Patient ID	Gender	Severity Level	Age	Blood Pressure
101	Male	High	45	120.5

Now classify each column:

Gender → Nominal

Severity Level → Ordinal

Age → Discrete (if recorded in whole years)

Blood Pressure → Continuous

Now we know:

For Age & Blood Pressure → We can calculate mean and standard deviation

For Gender → We use frequency count

For Severity → We analyze ranking

This is why identifying data type is critical.

⚠️ Common Beginner Mistakes

❌ Taking average of categorical data
❌ Treating ordinal data like continuous data
❌ Confusing discrete and continuous
❌ Applying wrong statistical tests

🧠 Why This Chapter Matters in Data Science

Understanding data types helps in:

Choosing correct visualization

Bar chart → Categorical

Histogram → Numerical

Selecting correct statistical test

Feature engineering

Data preprocessing

Model selection

Machine learning starts with proper data understanding.

🏁 Final Comparison Table
Main Type	Subtype	Example	Can Calculate Mean?
Qualitative	Nominal	Gender	❌
Qualitative	Ordinal	Rating (1–5)	❌
Quantitative	Discrete	Number of students	✅
Quantitative	Continuous	Height, Weight	✅
🔥 Easy Memory Trick

Nominal → Name

Ordinal → Order

Discrete → Digits (Counting)

Continuous → Continuum (Range)
