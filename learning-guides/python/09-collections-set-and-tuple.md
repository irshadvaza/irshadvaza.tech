📘 Chapter 9 – Collections (Part 2: Set and Tuple)
🔷 Part 1 – Set in Python
🌟 What is a Set?

A Set is a collection that:

❌ Does NOT allow duplicate values

❌ Does NOT support indexing

❌ Is unordered

✅ Stores only unique values

✅ Uses curly brackets {}

🟢 Creating a Set
myset = {10, 20, 30, 40}
print(myset)


Output (order may change):

{40, 10, 20, 30}


⚠ Important: Order is not guaranteed.

🔥 Main Difference Between List and Set
Feature	List	Set
Duplicate allowed?	✅ Yes	❌ No
Ordered?	✅ Yes	❌ No
Index supported?	✅ Yes	❌ No
Brackets	[]	{}
🧪 Example: Duplicate Values
mylist = [10, 20, 20, 30, 30, 30]
print(mylist)


Output:

[10, 20, 20, 30, 30, 30]


Now with Set:

myset = {10, 20, 20, 30, 30, 30}
print(myset)


Output:

{10, 20, 30}


✅ Set automatically removes duplicates.

🎯 Exam Question Type
❓ If you have a list and want unique values, how?
✅ Convert List to Set
mylist = [10, 20, 20, 30, 40, 40]

unique_values = set(mylist)

print(unique_values)


Output:

{10, 20, 30, 40}

⚠ Convert Back to List (Optional)
unique_list = list(set(mylist))
print(unique_list)

➕ Set Operations (Very Important for Exams)
✅ Union (Combine Two Sets)
set1 = {1, 2, 3}
set2 = {3, 4, 5}

result = set1.union(set2)
print(result)


Output:

{1, 2, 3, 4, 5}


Or using |

print(set1 | set2)

✅ Difference (Values in First but Not in Second)
set1 = {1, 2, 3}
set2 = {2, 3, 4}

print(set1.difference(set2))


Output:

{1}


Or:

print(set1 - set2)

✅ Intersection (Common Values)
print(set1.intersection(set2))


Output:

{2, 3}

➕ Adding & Removing in Set
✅ Add Element
myset = {10, 20}
myset.add(30)
print(myset)

✅ Remove Element
myset.remove(20)


⚠ If value not found → error

Safer option:

myset.discard(20)

📌 When Should We Use Set?

Use Set when:

You want unique values

You don’t care about order

You want fast membership testing

You want mathematical operations (union, intersection)

🔷 Part 2 – Tuple in Python
🌟 What is a Tuple?

A Tuple is:

Ordered

Allows duplicates

Cannot be changed (Immutable)

Written using round brackets ()

🟢 Creating a Tuple
mytuple = (10, 20, 30)
print(mytuple)

🔐 Why Tuple is Special?

Tuple is Immutable

That means:

❌ You cannot change values
❌ You cannot add/remove elements

❌ Example (Error)
mytuple = (10, 20, 30)
mytuple[1] = 99   # This will give error

📌 Tuple as Record

Tuple is often used to store related data (like database record).

Example:

student = ("Irshad", 101, "Data Science")

print(student[0])  # Name
print(student[1])  # ID
print(student[2])  # Course


Output:

Irshad
101
Data Science


Think of Tuple like:

📄 A fixed record
📦 A sealed box

📊 Difference Between List, Set and Tuple
Feature	List	Set	Tuple
Brackets	[]	{}	()
Ordered	✅ Yes	❌ No	✅ Yes
Duplicate allowed	✅ Yes	❌ No	✅ Yes
Index supported	✅ Yes	❌ No	✅ Yes
Mutable	✅ Yes	✅ Yes	❌ No
Best Use	General storage	Unique values	Fixed records
🎯 Exam Practice Questions
1️⃣ Remove Duplicate From List
numbers = [1, 2, 2, 3, 3, 4]
print(list(set(numbers)))

2️⃣ Find Union of Two Sets
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)

3️⃣ Find Difference
a = {1, 2, 3}
b = {2, 3}

print(a - b)

4️⃣ Access Second Element of Tuple
t = (100, 200, 300)
print(t[1])

🧠 Quick Revision
Use List:

When you need ordered & changeable data

Use Set:

When you need unique values

Use Tuple:

When data should not change (fixed record)

🚀 Next Chapter

Next we will learn:

📘 Dictionary (Very Important Collection in Python)
