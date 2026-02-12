📘 Chapter 12 – Advanced Data Visualization (Step-by-Step Upgrade 📊🚀)
🎯 What We Will Learn in This Chapter

In this chapter, we will cover:

✅ Pie Chart

✅ Histogram

✅ Scatter Plot

✅ Box Plot

✅ Real Dataset Example

✅ Pandas + Visualization

Now we move from basic plotting to real data understanding.

🥧 1️⃣ Pie Chart (Showing Percentage Distribution)
🌟 When to Use Pie Chart?

Use pie chart when:

You want to show percentage

You want to show proportion

Example: Subject weightage

🟢 Example – Study Time Distribution
import matplotlib.pyplot as plt

subjects = ["Math", "Science", "English", "Computer"]
hours = [4, 3, 2, 5]

plt.pie(hours, labels=subjects, autopct='%1.1f%%')
plt.title("Study Time Distribution")
plt.show()

🧠 Explanation

plt.pie() → Creates pie chart

labels= → Adds subject names

autopct → Shows percentage

%1.1f%% → 1 decimal percentage

📊 2️⃣ Histogram (Distribution of Data)
🌟 When to Use Histogram?

When you want to see:

Distribution of marks

Age distribution

Salary distribution

🟢 Example – Student Marks Distribution
marks = [45, 50, 67, 70, 72, 80, 85, 90, 95, 88, 76, 60]

plt.hist(marks, bins=5)
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()

🧠 Explanation

plt.hist() → Creates histogram

bins=5 → Divides data into 5 groups

Shows how many students fall into each range

🎯 3️⃣ Scatter Plot (Relationship Between Two Variables)
🌟 When to Use Scatter Plot?

When you want to see:

Relationship between study hours and marks

Height vs Weight

Experience vs Salary

🟢 Example – Study Hours vs Marks
hours = [1, 2, 3, 4, 5, 6, 7]
marks = [50, 55, 65, 70, 75, 85, 90]

plt.scatter(hours, marks)
plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.show()

🧠 What This Graph Shows?

If dots go upward → positive relationship
More study hours → more marks

This is basic foundation of Machine Learning thinking.

📦 4️⃣ Box Plot (Understanding Spread & Outliers)
🌟 When to Use Box Plot?

To understand:

Minimum value

Maximum value

Median

Outliers

🟢 Example
marks = [45, 50, 60, 70, 75, 80, 85, 90, 95, 100]

plt.boxplot(marks)
plt.title("Marks Box Plot")
plt.show()

🧠 What Student Should Observe?

Middle line → Median

Box → Middle 50% data

Lines → Range

Dots outside → Outliers

Very important for Data Science.

📊 5️⃣ Real Dataset Example Using Pandas

Now we move to real-world workflow.

🟢 Step 1 – Import Pandas
import pandas as pd
import matplotlib.pyplot as plt

🟢 Step 2 – Create Dataset
data = {
    "Name": ["Ali", "Sara", "Ahmed", "Fatima", "John"],
    "Math": [85, 90, 78, 88, 95],
    "Science": [80, 85, 88, 92, 89]
}

df = pd.DataFrame(data)

print(df)

🟢 Step 3 – Bar Chart Using Pandas
df.plot(x="Name", y=["Math", "Science"], kind="bar")
plt.title("Student Marks Comparison")
plt.show()

🧠 Explanation

df.plot() → Direct plotting from dataframe

x= → X-axis column

y= → Columns to compare

kind="bar" → Bar chart

📈 Pandas + Histogram
df["Math"].plot(kind="hist")
plt.title("Math Marks Distribution")
plt.show()

🎯 Pandas + Scatter Plot
df.plot(x="Math", y="Science", kind="scatter")
plt.title("Math vs Science")
plt.show()

🧠 Why Pandas Visualization is Powerful?

Because:

Real datasets are stored in DataFrame

You don’t manually create lists

You work with structured data

This is real Data Science workflow.


Since we are gradually increasing level, Count Plot is a very important addition — especially for categorical data.

⚠ Important Note:
countplot is from Seaborn, not pure matplotlib.

So now we will introduce Seaborn in very simple way.

You can add this section at the end of:

12-advanced-data-visualization.md


Below is the GitHub-ready Markdown content to append.

📊 6️⃣ Count Plot (Very Important for Categorical Data)
🌟 What is Count Plot?

A Count Plot shows:

👉 How many times each category appears.

It is mostly used for:

Gender count

Pass/Fail count

Product category count

Department distribution

🧠 Why Not Just Use Bar Chart?

You can use bar chart.

But count plot:

Automatically counts values

Cleaner syntax

Designed for categorical data

🛠 Step 1 – Install Seaborn
pip install seaborn

🟢 Step 2 – Import Seaborn
import seaborn as sns
import matplotlib.pyplot as plt

🟢 Example – Student Grade Categories
import seaborn as sns
import matplotlib.pyplot as plt

grades = ["A", "B", "A", "C", "B", "A", "B", "C", "A", "B"]

sns.countplot(x=grades)

plt.title("Grade Distribution")
plt.show()

🧠 Explanation (Line by Line)
sns.countplot(x=grades)

Automatically counts:

How many A

How many B

How many C

Displays frequency on Y-axis

You do NOT need to manually count.

Seaborn does it for you.

📊 Real Dataset Example with Pandas
import pandas as pd

data = {
    "Name": ["Ali", "Sara", "Ahmed", "Fatima", "John", "Zara"],
    "Gender": ["Male", "Female", "Male", "Female", "Male", "Female"]
}

df = pd.DataFrame(data)

sns.countplot(x="Gender", data=df)

plt.title("Gender Distribution")
plt.show()

🧠 What This Graph Shows?

How many Male

How many Female

Very common in:

HR Analytics

Survey Analysis

EDA projects

🎯 When to Use Count Plot?

Use count plot when:

Data is categorical

You want frequency

You want quick summary of categories

📌 Difference Between Bar Plot and Count Plot
Feature	Bar Plot	Count Plot
Need manual values?	✅ Yes	❌ No
Automatically counts?	❌ No	✅ Yes
Library	Matplotlib	Seaborn
Best For	Custom data	Categorical frequency
🎓 Practice Exercise

1️⃣ Create count plot for:

["Pass", "Fail", "Pass", "Pass", "Fail"]


2️⃣ Create count plot for department column in a dataframe.

🚀 Important Teaching Note For You

When explaining count plot:

Ask student:

“How many A grades do we have?”

Then show count plot.

This builds:

✔ Logical thinking
✔ Data understanding
✔ Interpretation skill


📌 Comparison Summary
Plot Type	Use Case
Bar Chart	Compare categories
Pie Chart	Percentage distribution
Histogram	Distribution
Scatter	Relationship
Box Plot	Spread & Outliers
🎓 Practice Tasks
1️⃣ Create Pie Chart for 5 students attendance.
2️⃣ Create Histogram of 20 random marks.
3️⃣ Create Scatter Plot of age vs salary.
4️⃣ Create Box Plot for 15 values.
