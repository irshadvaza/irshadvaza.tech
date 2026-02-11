📘 Chapter 8 – Collections in Python (Part 1: List)
🌟 What is a Collection?

Until now, we stored data like this:

x = 10
name = "Irshad"


But what if we want to store:

5 student marks

10 product prices

100 sensor readings

Instead of writing:

a = 10
b = 20
c = 30
d = 40
e = 50


Python gives us something better.

👉 A Collection

A collection allows us to store multiple values in a single variable.

✅ List (Most Common Collection in Python)

A List is:

Ordered

Changeable (Mutable)

Allows duplicate values

Written using square brackets []

🟢 Creating a List
mynum = [10, 20, 30, 40, 50]


This list contains 5 elements.

🔢 Index in List

Very Important Rule:

👉 Index starts from 0

Value	Index
10	0
20	1
30	2
40	3
50	4
📌 Accessing Elements
✅ First Element
print(mynum[0])


Output:

10

✅ Last Element (Two Ways)
print(mynum[4])
print(mynum[-1])


Output:

50
50


👉 -1 means last element
👉 -2 means second last

✂️ Slicing (Selecting Range of Values)
✅ Get elements from index 1 to 2
print(mynum[1:3])


Output:

[20, 30]


⚠ Important:

1:3 means:

Start at index 1

Stop before index 3

✅ Get alternate elements
print(mynum[1:5:2])


Output:

[20, 40]


Format:

[start : stop : step]

✅ Get elements from index 2 to end
print(mynum[2:])


Output:

[30, 40, 50]

📏 Length of List
print(len(mynum))


Output:

5

⚠ Important Note

Index starts from 0

len() counts total elements starting from 1

If list has 5 items:

Last index = 4

Length = 5

Very important for exams.

🔍 Check Value Using in
print(20 in mynum)


Output:

True

print(100 in mynum)


Output:

False

➕ Adding Elements to List
✅ append() – Add at End
mynum.append(60)
print(mynum)


Output:

[10, 20, 30, 40, 50, 60]

✅ insert() – Add at Specific Index
mynum.insert(2, 25)
print(mynum)


Output:

[10, 20, 25, 30, 40, 50, 60]

➕ Append One List to Another
lst1 = [10, 20, 30]
lst2 = [40, 50, 60]

lst1.append(lst2)

print(lst1)


Output:

[10, 20, 30, [40, 50, 60]]


⚠ Important:

append() adds the entire list as a single element.

❌ Removing Elements
✅ pop() – Remove by Index

Remove last element:

mynum.pop()


Remove specific index:

mynum.pop(2)

✅ remove() – Remove by Value
mynum.remove(30)


Removes first occurrence of 30.

✅ clear() – Remove All Elements
mynum.clear()
print(mynum)


Output:

[]

🔢 Useful List Methods
✅ count()
numbers = [10, 20, 20, 30, 20]
print(numbers.count(20))


Output:

3

✅ copy()
newlist = numbers.copy()
print(newlist)


Creates a duplicate list.

✅ reverse()
numbers.reverse()
print(numbers)


Reverses order.

✅ sort()
numbers.sort()
print(numbers)


Sorts in ascending order.

🔄 Updating List Values

Lists are mutable (changeable).

mynum = [10, 20, 30]
mynum[1] = 99
print(mynum)


Output:

[10, 99, 30]

🧠 Exam Practice Questions
1️⃣ Print Second Last Element
mynum = [10, 20, 30, 40, 50]
print(mynum[-2])

2️⃣ Add 100 at Index 1
mynum.insert(1, 100)

3️⃣ Remove First Occurrence of 20
mynum.remove(20)

4️⃣ Print Only Alternate Elements
mynum = [10, 20, 30, 40, 50]
print(mynum[::2])

📌 Chapter Summary

A List:

Uses square brackets []

Is ordered

Allows duplicates

Can be modified (mutable)

Index starts from 0

Common List Methods:

append()

insert()

pop()

remove()

clear()

count()

copy()

reverse()

sort()
