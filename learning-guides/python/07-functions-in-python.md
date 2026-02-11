# 📘 Chapter 7: Functions in Python 🧠
### _Organize Your Code & Reuse it Easily_

---

## 🎯 What You Will Learn

By the end of this chapter, you will understand:

- What a function is
- How to define and call functions
- How to pass parameters and get results
- Default parameters
- Local vs global variables
- Practice exercises and a mini project

---

# 🧩 1. What is a Function?

A function is like a **machine**:

- You give it some input
- It does some work
- It gives you output

Example in real life:
- Coffee machine → input: coffee powder + water → output: coffee  
- Function in Python → input: numbers → output: result

💡 Why functions?  
- Avoid repeating code  
- Make code organized  
- Easy to read and maintain  

---

# 🔹 2. Defining a Function

Syntax:

```python
def function_name(parameters):
    # code block
    return result  # optional
Example 1: Simple Greeting Function
def greet():
    print("Hello, welcome to Python Functions!")
Call the function:

greet()
Output:

Hello, welcome to Python Functions!
💡 def → defines the function, greet() → calls the function

🔹 3. Function with Parameters
Parameters let us pass information to functions.

def greet_user(name):
    print(f"Hello {name}, welcome to Python!")
Call it:

greet_user("Irshad")
greet_user("Alice")
Output:

Hello Irshad, welcome to Python!
Hello Alice, welcome to Python!
🔹 4. Function with Return Value
Sometimes we want a result back:

def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print("Sum is:", result)
Output:

Sum is: 8
💡 return → sends result back to the caller

🔹 5. Default Parameters
Functions can have optional parameters:

def greet_user(name="Student"):
    print(f"Hello {name}!")

greet_user("Alice")
greet_user()  # uses default
Output:

Hello Alice!
Hello Student!
🔹 6. Local vs Global Variables
Local variables → exist inside the function only

Global variables → exist outside functions, accessible everywhere

x = 10  # global

def demo():
    y = 5  # local
    print("Inside function:", x + y)

demo()
print("Outside function:", x)
# print(y)  # ❌ Error! y is local
Output:

Inside function: 15
Outside function: 10

# 🔹 7a. Using input() with Functions

The `input()` function allows the user to **enter data** while the program is running.

- By default, **input() returns a string**  
- You may need to **convert it** to int or float for calculations

---

### Example 1: Greeting User by Name

```python
def greet_user():
    name = input("Enter your name: ")
    print(f"Hello {name}, welcome to Python Functions!")
    
greet_user()
Output (example):

Enter your name: Irshad
Hello Irshad, welcome to Python Functions!
Example 2: Function with Input for Calculation
def add_numbers():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    print(f"The sum is {a + b}")

add_numbers()
Output (example):

Enter first number: 10
Enter second number: 5
The sum is 15
💡 Tip: Always convert input to int or float when doing math.

Example 3: Interactive Calculator Using Input
def calculator():
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    operation = input("Choose operation (+, -, *, /): ")

    if operation == "+":
        print(f"Result: {x + y}")
    elif operation == "-":
        print(f"Result: {x - y}")
    elif operation == "*":
        print(f"Result: {x * y}")
    elif operation == "/":
        if y != 0:
            print(f"Result: {x / y}")
        else:
            print("Cannot divide by zero")
    else:
        print("Invalid operation")

calculator()
Sample Output:

Enter first number: 12
Enter second number: 3
Choose operation (+, -, *, /): /
Result: 4.0



🧪 7. Practice Worksheet
✅ Exercise 1: Create a function to square a number
# define function square(num)
# return num*num
✅ Exercise 2: Greet multiple users
# define function greet_users(names)
# iterate over names and greet each
✅ Exercise 3: Function to calculate factorial (using loop)
# define factorial(n)
# use a for loop to calculate
🚀 8. Mini Project: Calculator Using Functions
Create a simple calculator with add, subtract, multiply, divide:

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"

# Using the calculator
x = 10
y = 5
print("Add:", add(x, y))
print("Subtract:", subtract(x, y))
print("Multiply:", multiply(x, y))
print("Divide:", divide(x, y))
Output:

Add: 15
Subtract: 5
Multiply: 50
Divide: 2.0
💡 Students can expand this with input from user and while loop for repeated calculation.

📌 Chapter Summary
✔ Functions are reusable blocks of code
✔ Use parameters to pass data
✔ Use return to get results
✔ Default parameters make functions flexible
✔ Local vs global variables control scope
✔ Mini projects help practice loops + functions
