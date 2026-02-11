# Chapter 4: Operators in Python 🧮  
*(Calculator-Style & Beginner Friendly)*

> **Goal of this chapter**  
> By the end of this chapter, you will:
> - Understand what **operators** are
> - Use Python like a **calculator**
> - Perform **math operations**
> - Compare values
> - Make simple decisions using logic

---

## 1. What is an Operator? 🤔

> An **operator** is a symbol that tells Python to **perform an action**.

In simple words:
- Operator = **Action**
- Values = **Things to act on**

---

## 2. Real-Life Example (Very Simple)

Think about a calculator:

| Symbol | Meaning |
|------|--------|
| + | Add |
| - | Subtract |
| × | Multiply |
| ÷ | Divide |

Python uses **almost the same symbols**.

---

## 3. Arithmetic Operators (Math Operators) ➕➖✖️➗

These are used for **calculations**.

### 3.1 Addition (+)

```python
total = 10 + 5
print(total)
Output:

15
👉 Example:

Total students = boys + girls

3.2 Subtraction (-)
balance = 100 - 30
print(balance)
Output:

70
👉 Example:

Wallet money after shopping

3.3 Multiplication (*)
price = 20 * 3
print(price)
Output:

60
👉 Example:

Price of 3 tickets

3.4 Division (/)
result = 10 / 2
print(result)
Output:

5.0
👉 Python always returns decimal for division.

3.5 Floor Division (//)
result = 10 // 3
print(result)
Output:

3
👉 Removes decimal part.

3.6 Modulus (%) – Remainder
remainder = 10 % 3
print(remainder)
Output:

1
👉 Used to check:

Even / Odd numbers

Divisibility

3.7 Power (**)
square = 5 ** 2
print(square)
Output:

25
👉 Example:

Area calculations

Mathematical formulas

4. Summary: Arithmetic Operators
Operator	Meaning
+	Addition
-	Subtraction
*	Multiplication
/	Division
//	Floor Division
%	Remainder
**	Power
5. Comparison Operators (Compare Values) ⚖️
These operators compare two values and return True or False.

5.1 Equal to (==)
print(10 == 10)
Output:

True
5.2 Not Equal (!=)
print(10 != 5)
Output:

True
5.3 Greater Than (>)
print(20 > 10)
Output:

True
5.4 Less Than (<)
print(5 < 3)
Output:

False
5.5 Greater Than or Equal (>=)
print(18 >= 18)
Output:

True
5.6 Less Than or Equal (<=)
print(15 <= 10)
Output:

False
6. Where Comparison Operators Are Used?
Checking age eligibility

Exam pass/fail

Price comparison

Data filtering

👉 Very important for if conditions (next chapter).

7. Logical Operators (Thinking Operators) 🧠
Used when multiple conditions are involved.

7.1 AND (and)
age = 20
has_id = True

print(age >= 18 and has_id)
Output:

True
👉 Both conditions must be True.

7.2 OR (or)
print(age < 18 or has_id)
Output:

True
👉 At least one condition must be True.

7.3 NOT (not)
is_raining = False
print(not is_raining)
Output:

True
👉 Reverses the result.

8. Operator Precedence (Simple Idea)
Python follows math rules.

result = 10 + 5 * 2
print(result)
Output:

20
👉 Multiplication happens before addition.

9. Real-Life Mini Example 🏪
price = 50
quantity = 3
total = price * quantity

print("Total bill:", total)
print("Is bill above 100?", total > 100)
Output:

Total bill: 150
Is bill above 100? True
10. Common Beginner Mistakes ⚠️
❌ Using = instead of ==

5 = 5   # Wrong
✅ Correct:

5 == 5
❌ Forgetting operator symbols

10 2   # Wrong
11. Practice Time ✍️
Try these:

a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a % b)
print(a > b)

