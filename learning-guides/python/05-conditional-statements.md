🎯 What You Will Learn

By the end of this chapter, you will be able to:

Understand decision-making in Python

Use if, else, and elif confidently

Read Python code like plain English

Solve real-life problems using conditions

Build small decision-based programs

🧠 What Are Conditional Statements?

👉 Conditional statements allow Python to make decisions

In real life, we think like this:

If it rains → take an umbrella
Else → enjoy the sunshine

Python thinks exactly the same way 🌦️

🧩 Simple English → Python Logic
English Thinking	Python Code
If condition is true	if
Otherwise	else
Multiple conditions	elif
🚦 1. The if Statement
One Condition, One Decision
🔍 Syntax (Very Simple)
if condition:
    action


📌 Python reads this as:

If condition is true → do this

✏️ Example 1: Age Check
age = 20

if age >= 18:
    print("You are eligible to vote")


🖨 Output:

You are eligible to vote


🧠 Explanation:

Age is 20

20 ≥ 18 → True

Python executes the print statement

🧱 Important Rule: Indentation ⚠️

Python uses spaces (indentation) instead of brackets {}.

❌ Wrong:

if age >= 18:
print("Eligible")


✅ Correct:

if age >= 18:
    print("Eligible")


📌 Think of indentation as belonging to the decision

🔀 2. The if - else Statement
Yes or No Decision
🧠 Real-Life Thinking

If marks ≥ 40 → Pass
Else → Fail

✏️ Example 2: Pass or Fail
marks = 35

if marks >= 40:
    print("You Passed 🎉")
else:
    print("You Failed ❌")


🖨 Output:

You Failed ❌

🪜 3. The elif Statement
Multiple Conditions
🧠 Real-Life Example

If score ≥ 90 → Grade A
Else if score ≥ 75 → Grade B
Else → Grade C

✏️ Example 3: Grade System
score = 82

if score >= 90:
    print("Grade A")
elif score >= 75:
    print("Grade B")
else:
    print("Grade C")


🖨 Output:

Grade B

🔄 How Python Checks Conditions (Flow)

1️⃣ Check if
2️⃣ If false → check elif
3️⃣ If all false → execute else

📌 Python stops checking after first True condition

🔗 4. Using Logical Operators with Conditions
✏️ Example 4: Login Check
username = "admin"
password = "1234"

if username == "admin" and password == "1234":
    print("Login Successful ✅")
else:
    print("Invalid Credentials ❌")

🧪 Practice Section (Try Yourself)
📝 Exercise 1: Temperature Check
temperature = 30

# If temperature >= 35 → print "Very Hot"
# Else → print "Normal Weather"

📝 Exercise 2: Even or Odd
number = 7

# Check if number is even or odd

📝 Exercise 3: Ticket Pricing
age = 12

# If age < 12 → price = 5
# If age between 12 and 60 → price = 10
# Else → price = 7

🚀 MINI PROJECT: Smart ATM Message 💳
🎯 Problem

Display message based on balance amount

🧠 Logic

Balance ≥ 5000 → VIP Customer

Balance ≥ 1000 → Normal Customer

Else → Low Balance Warning

✅ Solution Code
balance = 3200

if balance >= 5000:
    print("VIP Customer 🌟")
elif balance >= 1000:
    print("Normal Customer 🙂")
else:
    print("Low Balance ⚠️")

🌍 Real-World Applications

Conditional statements are used in:

🏦 Banking systems

🔐 Login systems

🛒 E-commerce discounts

📊 Data filtering

🤖 AI decision making

📌 Common Beginner Mistakes

❌ Using = instead of ==
❌ Missing indentation
❌ Wrong condition order

✅ Always test conditions from highest to lowest

🧠 Chapter Summary

✔ Python uses conditions to think
✔ if → decision
✔ elif → another condition
✔ else → default action
✔ Indentation is mandatory
