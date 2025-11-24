# This script demonstrates the itertools module
# itertools provides efficient iterators for common programming patterns

import itertools

# count() - infinite counter
print("=== count() - Infinite Counter ===")
counter = itertools.count(start=10, step=2)
print("First 5 values:", [next(counter) for _ in range(5)])
print()


# cycle() - infinite cycling through an iterable
print("=== cycle() - Infinite Cycling ===")
colors = itertools.cycle(['red', 'green', 'blue'])
print("Cycling through colors:", [next(colors) for _ in range(7)])
print()


# repeat() - repeat an element
print("=== repeat() - Repeat Element ===")
repeated = list(itertools.repeat("Hello", 3))
print(f"Repeated: {repeated}")

# Useful with map() - multiply each number by 2
numbers = [1, 2, 3, 4, 5]
doubled = list(map(pow, numbers, itertools.repeat(2)))
print(f"Squared using repeat: {doubled}")
print()


# chain() - combine multiple iterables
print("=== chain() - Combine Iterables ===")
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [10, 20]
combined = list(itertools.chain(list1, list2, list3))
print(f"Chained: {combined}")

# chain.from_iterable - flatten one level
nested = [[1, 2], [3, 4], [5, 6]]
flattened = list(itertools.chain.from_iterable(nested))
print(f"Flattened: {flattened}")
print()


# islice() - slice an iterator
print("=== islice() - Slice Iterator ===")
numbers = range(100)
sliced = list(itertools.islice(numbers, 5, 15, 2))  # start, stop, step
print(f"Sliced (5:15:2): {sliced}")
print()


# compress() - filter using selector
print("=== compress() - Filter with Selectors ===")
data = ['a', 'b', 'c', 'd', 'e']
selectors = [True, False, True, False, True]
result = list(itertools.compress(data, selectors))
print(f"Compressed: {result}")
print()


# takewhile() and dropwhile()
print("=== takewhile() and dropwhile() ===")
numbers = [1, 3, 5, 7, 4, 2, 6, 8]
taken = list(itertools.takewhile(lambda x: x < 6, numbers))
dropped = list(itertools.dropwhile(lambda x: x < 6, numbers))
print(f"Original: {numbers}")
print(f"takewhile(x < 6): {taken}")
print(f"dropwhile(x < 6): {dropped}")
print()


# groupby() - group consecutive elements
print("=== groupby() - Group Consecutive ===")
data = [('a', 1), ('a', 2), ('b', 3), ('b', 4), ('a', 5)]
# Must be sorted for groupby to work properly!
sorted_data = sorted(data, key=lambda x: x[0])
for key, group in itertools.groupby(sorted_data, key=lambda x: x[0]):
    print(f"  Key '{key}': {list(group)}")

# Grouping numbers by property
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for is_even, group in itertools.groupby(sorted(numbers, key=lambda x: x % 2), key=lambda x: x % 2 == 0):
    label = "Even" if is_even else "Odd"
    print(f"  {label}: {list(group)}")
print()


# permutations() - all possible orderings
print("=== permutations() - All Orderings ===")
items = ['A', 'B', 'C']
perms = list(itertools.permutations(items))
print(f"Permutations of {items}:")
for p in perms:
    print(f"  {p}")

# Permutations of specific length
perms_2 = list(itertools.permutations(items, 2))
print(f"Permutations of length 2: {perms_2}")
print()


# combinations() - unique combinations (order doesn't matter)
print("=== combinations() - Unique Combinations ===")
items = ['A', 'B', 'C', 'D']
combs = list(itertools.combinations(items, 2))
print(f"Combinations of 2 from {items}: {combs}")

combs_3 = list(itertools.combinations(items, 3))
print(f"Combinations of 3: {combs_3}")
print()


# combinations_with_replacement() - combinations with repetition
print("=== combinations_with_replacement() ===")
items = ['A', 'B', 'C']
combs = list(itertools.combinations_with_replacement(items, 2))
print(f"Combinations with replacement: {combs}")
print()


# product() - cartesian product
print("=== product() - Cartesian Product ===")
colors = ['red', 'blue']
sizes = ['S', 'M', 'L']
products = list(itertools.product(colors, sizes))
print(f"All color-size combinations: {products}")

# Product with repeat
dice = list(itertools.product(range(1, 7), repeat=2))
print(f"All two-dice combinations: {len(dice)} total")
print(f"First 6: {dice[:6]}")
print()


# accumulate() - cumulative results
print("=== accumulate() - Cumulative Results ===")
numbers = [1, 2, 3, 4, 5]
cumsum = list(itertools.accumulate(numbers))
print(f"Cumulative sum: {cumsum}")

import operator
cumprod = list(itertools.accumulate(numbers, operator.mul))
print(f"Cumulative product: {cumprod}")

# Running maximum
data = [3, 1, 4, 1, 5, 9, 2, 6]
running_max = list(itertools.accumulate(data, max))
print(f"Running maximum: {running_max}")
print()


# starmap() - apply function to pre-zipped arguments
print("=== starmap() - Apply to Argument Tuples ===")
pairs = [(2, 3), (4, 5), (6, 7)]
results = list(itertools.starmap(pow, pairs))
print(f"Powers {pairs}: {results}")

coordinates = [(1, 2), (3, 4), (5, 6)]
distances = list(itertools.starmap(lambda x, y: (x**2 + y**2)**0.5, coordinates))
print(f"Distances from origin: {distances}")
print()


# Practical example: Generate all possible passwords
print("=== Practical: Password Generator ===")
chars = 'ab12'
length = 2
passwords = [''.join(p) for p in itertools.product(chars, repeat=length)]
print(f"All {length}-char passwords from '{chars}': {passwords}")

