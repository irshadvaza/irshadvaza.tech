# Chapter 3: Variables & Data Types (Super Easy & Fun)

> **Goal of this chapter**  
> By the end of this chapter, you will:
> - Understand **what a variable is**
> - Learn **why variables are needed**
> - Understand **different data types**
> - Write simple Python programs confidently

---

## 1. What is a Variable? 🍕

### Variables are like **labeled pizza boxes**

Imagine you order pizzas 🍕 and keep them in boxes.

Each box:
- Has a **label**
- Contains something inside

In Python:
- The **label** is called a **variable**
- The **content** is called a **value**

👉 A variable stores information so we can use it later.

---

## 2. Real-Life Example (Very Important)

Think about this:

- You remember your **name**
- You remember your **age**
- You remember whether it is **hot or cold**

Python does the same using variables.

---

## 3. Creating Your First Variable 🧑‍💻

```python
name = "Irshad"
age = 30
is_student = True
Explanation:
name → variable name

"Irshad" → value

= → assignment (store value)

👉 Python reads this as:

“Store the value on the right inside the name on the left.”

4. Pizza Box Example (Best for Beginners 🍕)
toppings = "pepperoni"   # String (text)
price = 12.99            # Float (decimal)
is_hot = True            # Boolean (True/False)
👉 Each variable stores different type of data.

5. Rules for Naming Variables 📏
Python is flexible, but there are rules:

✅ Allowed
age = 25
student_name = "Ali"
price_2024 = 100
❌ Not Allowed
2age = 25        # Cannot start with number
student-name = "Ali"   # No hyphens
class = "Math"  # Reserved word
Best Practice 👍
Use meaningful names

Use lowercase

Use underscores

6. What is a Data Type? 📦
A data type tells Python what kind of data is stored in a variable.

Python automatically understands data types.

7. Common Data Types in Python
1️⃣ String (Text) 📝
Used for:

Names

Messages

Sentences

city = "Abu Dhabi"
course = "Data Science"
👉 Strings are written inside quotes.

2️⃣ Integer (Whole Numbers) 🔢
Used for:

Age

Count

Quantity

students = 25
days = 7
3️⃣ Float (Decimal Numbers) 📐
Used for:

Price

Temperature

Marks

price = 12.99
temperature = 36.5
4️⃣ Boolean (True / False) ✅❌
Used for:

Yes / No

On / Off

True / False

is_hot = True
is_raining = False
👉 Boolean values are capitalized: True, False

8. Checking the Data Type 🔍
Python provides a built-in function:

type(price)
Output:

<class 'float'>
9. Printing Variables 📤
name = "Aisha"
age = 22

print(name)
print(age)
Output:

Aisha
22
10. Combining Text and Variables 🧠
name = "Ahmed"
age = 25

print("Name:", name)
print("Age:", age)
Output:

Name: Ahmed
Age: 25
11. Changing Variable Values 🔄
Variables can change.

score = 50
score = 80

print(score)
Output:

80
👉 Python always keeps the latest value.

12. Why Variables Are Important in Data Science 📊
In Data Science, variables store:

Data values

Results

Predictions

Calculations

Without variables:
❌ No analysis
❌ No machine learning
❌ No AI

13. Common Beginner Mistakes ⚠️
❌ Forgetting quotes:

name = Irshad   # Wrong
✅ Correct:

name = "Irshad"
❌ Wrong boolean:

is_hot = true   # Wrong
✅ Correct:

is_hot = True
14. Practice Time ✍️
Try this yourself:

food = "Biryani"
price = 15.5
is_spicy = True

print(food)
print(price)
print(is_spicy)
