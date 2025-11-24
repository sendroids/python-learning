# This script demonstrates advanced comprehensions in Python
# Beyond basic list comprehensions: dict, set, and nested comprehensions

# Review: List comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"List comprehension (squares): {squares}")


# Dictionary comprehension
print("\n=== Dictionary Comprehensions ===")

# Basic dict comprehension
names = ["Alice", "Bob", "Charlie"]
name_lengths = {name: len(name) for name in names}
print(f"Name lengths: {name_lengths}")

# Dict comprehension with condition
numbers = range(1, 11)
even_squares = {n: n**2 for n in numbers if n % 2 == 0}
print(f"Even number squares: {even_squares}")

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"Swapped dict: {swapped}")

# Dict from two lists
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
combined = {k: v for k, v in zip(keys, values)}
print(f"Combined from lists: {combined}")


# Set comprehension
print("\n=== Set Comprehensions ===")

# Basic set comprehension
words = ["hello", "world", "hello", "python", "world"]
unique_lengths = {len(word) for word in words}
print(f"Unique word lengths: {unique_lengths}")

# Set comprehension with condition
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_evens = {n for n in numbers if n % 2 == 0}
print(f"Unique even numbers: {unique_evens}")

# First characters (unique)
names = ["Alice", "Anna", "Bob", "Charlie", "Chris"]
first_chars = {name[0] for name in names}
print(f"Unique first characters: {first_chars}")


# Nested comprehensions
print("\n=== Nested Comprehensions ===")

# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")

# Create a matrix
rows, cols = 3, 4
matrix = [[0 for _ in range(cols)] for _ in range(rows)]
print(f"3x4 zero matrix: {matrix}")

# Multiplication table
mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
print("5x5 Multiplication table:")
for row in mult_table:
    print(f"  {row}")

# Nested with condition
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
even_elements = [num for row in matrix for num in row if num % 2 == 0]
print(f"Even elements from matrix: {even_elements}")


# Comprehensions with multiple conditions
print("\n=== Multiple Conditions ===")

# Multiple conditions (AND)
numbers = range(1, 21)
divisible_by_2_and_3 = [n for n in numbers if n % 2 == 0 if n % 3 == 0]
print(f"Divisible by both 2 and 3: {divisible_by_2_and_3}")

# Multiple conditions using 'and'
same_result = [n for n in numbers if n % 2 == 0 and n % 3 == 0]
print(f"Same with 'and': {same_result}")

# Conditional expression in comprehension
labels = ["even" if n % 2 == 0 else "odd" for n in range(1, 6)]
print(f"Labels: {labels}")


# Comprehensions with function calls
print("\n=== Comprehensions with Functions ===")


def process(x):
    return x**2 + 1


processed = [process(x) for x in range(5)]
print(f"Processed values: {processed}")

# With lambda
transformed = [(lambda x: x * 2)(n) for n in range(5)]
print(f"Lambda transformed: {transformed}")


# Generator expression (memory efficient alternative)
print("\n=== Generator Expressions ===")

# Generator expression - like list comprehension but lazy
gen = (x**2 for x in range(1000000))
print(f"Generator object: {gen}")
print(f"First 5 values: {[next(gen) for _ in range(5)]}")

# Memory comparison
import sys
list_comp = [x**2 for x in range(1000)]
gen_exp = (x**2 for x in range(1000))
print(f"List size: {sys.getsizeof(list_comp)} bytes")
print(f"Generator size: {sys.getsizeof(gen_exp)} bytes")


# Practical examples
print("\n=== Practical Examples ===")

# Word frequency from sentences
sentences = ["the cat sat", "the dog ran", "the cat ran"]
words = [word for sentence in sentences for word in sentence.split()]
word_freq = {word: words.count(word) for word in set(words)}
print(f"Word frequency: {word_freq}")

# Filter and transform data
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 72},
    {"name": "Charlie", "score": 90},
    {"name": "David", "score": 68},
]

# Get names of passing students (score >= 75)
passing = [s["name"] for s in students if s["score"] >= 75]
print(f"Passing students: {passing}")

# Create grade mapping
grades = {s["name"]: "A" if s["score"] >= 90 else "B" if s["score"] >= 80 else "C" if s["score"] >= 70 else "D" for s in students}
print(f"Grades: {grades}")

