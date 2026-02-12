📘 Chapter 11 – Data Visualization in Python (From Zero to Confidence 📊)
🌟 What is Data Visualization?

Data Visualization means:

👉 Showing data using graphs and charts instead of only numbers.

Example:

Instead of this:

Math = 85
Science = 90
English = 78


We show it like a bar chart 📊

Because human brain understands visuals faster than numbers.

🎯 Why Data Visualization is Important?

Makes data easy to understand

Helps in decision making

Used in Data Science & Analytics

Used in dashboards (Power BI, Tableau, etc.)

Used in reports and presentations

🛠 Step 1 – Install Library

We will use:

matplotlib


Install using:

pip install matplotlib

🧠 What is matplotlib?

It is a Python library used to create:

Line charts

Bar charts

Pie charts

Scatter plots

Histograms

🟢 First Example – Student Marks (Bar Chart)
🎓 Our Data

We have 5 subjects:

Math

Science

English

Physics

Computer

Marks:

85, 90, 78, 88, 95

✨ Full Code (First Simple Graph)
import matplotlib.pyplot as plt

subjects = ["Math", "Science", "English", "Physics", "Computer"]
marks = [85, 90, 78, 88, 95]

plt.bar(subjects, marks)

plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.title("Student Marks Report")

plt.show()

🧠 Now Let’s Understand Line by Line
1️⃣ Import Library
import matplotlib.pyplot as plt


Meaning:

We are importing matplotlib

pyplot is the module for plotting

as plt means we give it short name

Think like nickname:

matplotlib.pyplot → plt

2️⃣ Create X-axis Data
subjects = ["Math", "Science", "English", "Physics", "Computer"]


This is a list.

These values will appear on:

👉 X-axis (horizontal line)

3️⃣ Create Y-axis Data
marks = [85, 90, 78, 88, 95]


These numbers will appear on:

👉 Y-axis (vertical line)

4️⃣ Create Bar Chart
plt.bar(subjects, marks)


Meaning:

Create bar graph

X-axis → subjects

Y-axis → marks

5️⃣ Add Labels
plt.xlabel("Subjects")
plt.ylabel("Marks")


This adds labels on:

X-axis

Y-axis

6️⃣ Add Title
plt.title("Student Marks Report")


Adds heading to graph.

7️⃣ Show Graph
plt.show()


Very important.

Without this, graph will not display.

📊 Output

You will see a bar chart like:

Bars showing marks

Subjects on bottom

Marks on side

Title on top

🔵 Second Example – Line Chart

Now let’s draw line chart.

plt.plot(subjects, marks)
plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.title("Student Marks Line Chart")
plt.show()


Difference:

plt.bar() → Bar graph

plt.plot() → Line graph

🟣 Third Example – Add Markers
plt.plot(subjects, marks, marker='o')
plt.show()


Marker means:

Put circle dot on each value.

🔴 Improve Graph (Make it Attractive)
plt.figure(figsize=(8,5))

plt.bar(subjects, marks)

plt.title("Student Marks Report", fontsize=14)
plt.xlabel("Subjects")
plt.ylabel("Marks")

plt.grid(True)

plt.show()


New thing:

plt.figure(figsize=(8,5))


This changes graph size.

📌 Practice Exercise
1️⃣ Create bar chart for:
Months = Jan, Feb, Mar, Apr
Sales = 1000, 1500, 1200, 1800

2️⃣ Create line chart with markers.
🎓 Mini Project – Compare Two Students
subjects = ["Math", "Science", "English"]

student1 = [80, 85, 78]
student2 = [88, 90, 92]

plt.plot(subjects, student1, marker='o')
plt.plot(subjects, student2, marker='o')

plt.legend(["Student 1", "Student 2"])

plt.title("Marks Comparison")
plt.show()

🧠 Key Learning

Today student learned:

What is data visualization

What is matplotlib

How to create:

Bar chart

Line chart

How to:

Add title

Add labels

Add grid

Add legend

Add markers

🚀 Next Step (Gradually Increase Level)

Next chapter we can cover:

Pie chart

Histogram

Scatter plot

Real dataset example

Pandas + Visualization
