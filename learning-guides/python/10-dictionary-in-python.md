📘 Chapter 10 – Dictionary in Python (Key–Value Power 🔑)
🌟 What is a Dictionary?

A Dictionary is a collection that stores data in:

Key : Value


It is like a real-world dictionary:

word → meaning


In Python:

key → value

📦 Real-Life Example

Student Record:

Name → Irshad

Age → 30

Course → Data Science

Instead of using list:

student = ["Irshad", 30, "Data Science"]


We use Dictionary:

student = {
    "name": "Irshad",
    "age": 30,
    "course": "Data Science"
}


Much clearer ✅

🧠 Key Features of Dictionary

Uses curly brackets { }

Stores data as key:value

Keys must be unique

Values can be duplicate

Mutable (can change data)

🔎 Accessing Dictionary Values
student = {
    "name": "Irshad",
    "age": 30,
    "course": "Data Science"
}

print(student["name"])


Output:

Irshad

➕ Adding New Item

Simply assign new key:

student["city"] = "Abu Dhabi"
print(student)


Output:

{'name': 'Irshad', 'age': 30, 'course': 'Data Science', 'city': 'Abu Dhabi'}

✏ Updating Existing Item
student["age"] = 31
print(student)


Now age is updated.

❌ Removing Item
✅ Using pop()
student.pop("course")
print(student)


Removes specific key.

✅ Using del
del student["city"]
print(student)

✅ Remove All Items
student.clear()
print(student)


Output:

{}

🔁 Loop Through Dictionary

Very Important for Exams 🔥

✅ Print Keys
for i in student.keys():
    print(i)

✅ Print Values
for j in student.values():
    print(j)

✅ Print Both Key and Value
for i, j in student.items():
    print(i, j)


Example Output:

name Irshad
age 31
course Data Science


Explanation:

.items() returns key-value pair

i → key

j → value

📊 Dictionary Methods
✅ Get Value Safely
print(student.get("name"))


If key not found → returns None (no error)

✅ Check if Key Exists
print("age" in student)


Output:

True

✅ Get All Keys
print(student.keys())

✅ Get All Values
print(student.values())

🎯 Exam Practice Questions
1️⃣ Add New Subject
marks = {"math": 90, "science": 85}
marks["english"] = 88
print(marks)

2️⃣ Update Math Marks
marks["math"] = 95

3️⃣ Remove Science
marks.pop("science")

4️⃣ Print All Key and Value
for subject, score in marks.items():
    print(subject, score)

🆚 Difference Between List, Set, Tuple and Dictionary
Feature	List	Set	Tuple	Dictionary
Brackets	[]	{}	()	{}
Ordered	✅ Yes	❌ No	✅ Yes	✅ Yes
Duplicate allowed	✅ Yes	❌ No	✅ Yes	Keys ❌ / Values ✅
Mutable	✅ Yes	✅ Yes	❌ No	✅ Yes
Stores	Values	Unique values	Fixed values	Key-Value pairs
🧠 When Should We Use Dictionary?

Use Dictionary when:

Data has label (key)

You want fast lookup

You store record-like data

You work with JSON/API data

📌 Chapter Summary

Dictionary:

Stores data as key:value

Keys must be unique

Mutable (can add, update, delete)

Very powerful for real-world data

🚀 What’s Next?
