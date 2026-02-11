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


-------------------------------------------------------------------------For Practice----------------------------------------------------
## 🏫 Extra Nested Loop Examples (Exam-Friendly) 📚

Nested loops are often asked in exams in **pattern printing**, **table generation**, or **simple repeated operations**.

---

### 🔹 Example 1: Print a Rectangle of Stars

**Problem:** Print a rectangle with 3 rows and 5 columns.

```python
rows = 3
cols = 5

for i in range(rows):
    for j in range(cols):
        print("*", end=" ")
    print()  # move to next line
Output:

* * * * * 
* * * * * 
* * * * * 
Explanation:

Outer loop → rows

Inner loop → columns

end=" " prevents new line after each star

print() moves to the next row

🔹 Example 2: Print a Right-Angled Triangle (Number Pattern)
Problem: Print numbers like this:

1
1 2
1 2 3
1 2 3 4
n = 4

for i in range(1, n + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()
Output:

1
1 2
1 2 3
1 2 3 4
Explanation:

Outer loop → row number

Inner loop → numbers from 1 to current row number

🔹 Example 3: Print a Multiplication Table (Nested Loop)
Problem: Print multiplication table for numbers 1 to 3

for i in range(1, 4):
    for j in range(1, 4):
        print(i, "x", j, "=", i * j)
    print("------")
Output:

1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
------
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
------
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
------
Explanation:

Outer loop → row (1, 2, 3)

Inner loop → column multiplier (1, 2, 3)

print("------") separates tables

🔹 Example 4: Print a Simple Pattern (Exam Classic)
Pattern:

A A A
B B B
C C C
rows = 3
letter = "A"

for i in range(rows):
    for j in range(3):
        print(letter, end=" ")
    print()
    letter = chr(ord(letter) + 1)
Output:

A A A
B B B
C C C
Explanation:

chr(ord(letter) + 1) → converts letter to next alphabet

Outer loop → controls row

Inner loop → prints letters in a row

🔹 Example 5: Exam Quick Question – Sum Table
Problem: Print sum of two numbers 1 to 3

for i in range(1, 4):
    for j in range(1, 4):
        print(i, "+", j, "=", i + j)
    print("------")
Output:

1 + 1 = 2
1 + 2 = 3
1 + 3 = 4
------
2 + 1 = 3
2 + 2 = 4
2 + 3 = 5
------
3 + 1 = 4
3 + 2 = 5
3 + 3 = 6
------
💡 Exam Tip: Questions like these are very common in nested loop / pattern printing exercises.

✅ Summary of Nested Loop Tips for Exams
Always identify outer and inner loops

Use end=" " to print in same line

Increment letters using chr(ord(letter) + 1)

Use loops for patterns, tables, or repeated calculations

Practice these examples; they cover 80% of typical exam questions 👌

