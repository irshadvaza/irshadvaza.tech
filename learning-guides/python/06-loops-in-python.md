# 📘 Chapter 6: Loops in Python 🔁  
### _Let Python Repeat Tasks Automatically_

---

## 🎯 What You Will Learn
By the end of this chapter, you will:
- Understand **what loops are**
- Learn **why loops are useful**
- Use `for` and `while` loops
- Combine loops with **conditions**
- Solve real-life tasks automatically

---

## 🧠 What is a Loop?

Think of loops like **robots that repeat tasks for you** 🤖

> Example: You have 10 dishes to wash  
> You can wash them **one by one manually**  
> OR tell a robot to **wash 10 dishes automatically**  

Python loops are **your programming robot**.

---

## 🔄 1. The `for` Loop (Counting Robot)

`for` loops are used when you **know how many times** you want to repeat a task.

---

### ✏️ Syntax

```python
for variable in sequence:
    action
🖥 Animation-Style Example
Imagine stack of 5 books, Python reads each book one by one:

books = ["Math", "Physics", "Chemistry", "English", "Biology"]

for book in books:
    print("Studying:", book)
🖨 Output:

Studying: Math
Studying: Physics
Studying: Chemistry
Studying: English
Studying: Biology
💡 Explanation: Python picks one item at a time and repeats the action

🔢 Example 2: Count 1 to 5
for i in range(1, 6):
    print("Number:", i)
🖨 Output:

Number: 1
Number: 2
Number: 3
Number: 4
Number: 5
💡 range(start, end) → includes start, excludes end

⏳ 2. The while Loop (Condition Robot)
while loops repeat as long as a condition is true

✏️ Syntax
while condition:
    action
🖥 Animation-Style Example: Countdown 🚀
count = 5

while count > 0:
    print("Countdown:", count)
    count -= 1
🖨 Output:

Countdown: 5
Countdown: 4
Countdown: 3
Countdown: 2
Countdown: 1
💡 Explanation:

Condition: count > 0

Python keeps repeating until condition is false

count -= 1 reduces value each time

🔗 3. Break & Continue (Control the Loop)
🔹 break → Stop the loop
for i in range(1, 10):
    if i == 5:
        break
    print(i)
Output:

1
2
3
4
💡 Loop stops at 5

🔹 continue → Skip one iteration
for i in range(1, 6):
    if i == 3:
        continue
    print(i)
Output:

1
2
4
5
💡 Skips printing 3, continues with next

🎨 4. Nested Loops (Loop Inside Loop)
Think of loops inside loops like a clock: hours → minutes → seconds

for i in range(1, 4):
    for j in range(1, 4):
        print(i, "-", j)
Output:

1 - 1
1 - 2
1 - 3
2 - 1
2 - 2
2 - 3
3 - 1
3 - 2
3 - 3
💡 Python repeats inner loop for each outer loop value

🧪 PRACTICE WORKSHEET
✅ Exercise 1: Print Numbers 1-10
# Use a for loop and range()
✅ Exercise 2: Print Even Numbers
# Use a for loop and if condition
✅ Exercise 3: Multiplication Table
# Print table of 5 using a loop
🚀 MINI PROJECT: Star Pattern ⭐
Problem
Print this pattern:

*
**
***
****
Solution
rows = 4

for i in range(1, rows + 1):
    print("*" * i)
Output:

*
**
***
****
💡 Explanation:

i increases each row

"*" multiplied by i → prints stars in a line

🌍 Real-Life Loop Examples
Counting items in a cart 🛒

Printing invoices 🧾

Repeating experiments in Data Science 📊

Animations & games 🎮

📌 Chapter Summary
✔ for → known repetitions
✔ while → repeat until condition is False
✔ break → stop loop
✔ continue → skip iteration
✔ Nested loops → loops inside loops

Loops = Python robot that saves your time 🤖

