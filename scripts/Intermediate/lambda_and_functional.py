# This script demonstrates lambda functions and functional programming
# Lambda functions are small anonymous functions defined with the lambda keyword

# Basic lambda syntax
square = lambda x: x ** 2
print(f"Square of 5: {square(5)}")

add = lambda a, b: a + b
print(f"3 + 7 = {add(3, 7)}")
print()


# Using lambda with map()
# map() applies a function to every item in an iterable
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))
print(f"Original: {numbers}")
print(f"Doubled: {doubled}")

# Convert strings to uppercase
words = ["hello", "world", "python"]
upper_words = list(map(lambda s: s.upper(), words))
print(f"Uppercase words: {upper_words}")
print()


# Using lambda with filter()
# filter() selects items that satisfy a condition
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {evens}")

# Filter strings by length
words = ["a", "cat", "is", "sleeping", "on", "couch"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(f"Words longer than 3 chars: {long_words}")
print()


# Using lambda with sorted()
# Sort by custom criteria
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
]

by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print("Students sorted by grade (highest first):")
for student in by_grade:
    print(f"  {student['name']}: {student['grade']}")
print()


# Using reduce() from functools
# reduce() applies a function cumulatively to items
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda a, b: a + b, numbers)
print(f"Sum of {numbers}: {total}")

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(f"Maximum: {maximum}")

# Concatenate strings
words = ["Python", "is", "awesome"]
sentence = reduce(lambda a, b: f"{a} {b}", words)
print(f"Sentence: {sentence}")
print()


# Combining map, filter, and reduce
# Find sum of squares of even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = reduce(
    lambda a, b: a + b,
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers))
)
print(f"Sum of squares of even numbers in {numbers}: {result}")
print()


# Using lambda with min() and max()
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]

youngest = min(people, key=lambda p: p[1])
oldest = max(people, key=lambda p: p[1])
print(f"Youngest: {youngest[0]}, age {youngest[1]}")
print(f"Oldest: {oldest[0]}, age {oldest[1]}")

