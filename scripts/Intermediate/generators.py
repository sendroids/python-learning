# This script demonstrates generators and the yield keyword
# Generators are memory-efficient iterators that generate values on-the-fly

# Basic generator function
def count_up_to(n):
    """Generate numbers from 1 to n."""
    i = 1
    while i <= n:
        yield i
        i += 1


print("Counting up to 5:")
for num in count_up_to(5):
    print(num)
print()


# Generator vs list - memory efficiency
def fibonacci_generator(limit):
    """Generate Fibonacci numbers up to a limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


print("Fibonacci numbers up to 100:")
print(list(fibonacci_generator(100)))
print()


# Generator expression (like list comprehension but lazy)
squares_list = [x**2 for x in range(10)]  # Creates entire list in memory
squares_gen = (x**2 for x in range(10))   # Creates generator object

print("List:", squares_list)
print("Generator object:", squares_gen)
print("Generator values:", list(squares_gen))
print()


# Using next() with generators
def simple_generator():
    yield "First"
    yield "Second"
    yield "Third"


gen = simple_generator()
print("Using next():")
print(next(gen))
print(next(gen))
print(next(gen))
print()


# Generator with send() - two-way communication
def accumulator():
    """Generator that accumulates values sent to it."""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value


acc = accumulator()
next(acc)  # Prime the generator
print("Accumulator example:")
print(f"Send 10: {acc.send(10)}")
print(f"Send 20: {acc.send(20)}")
print(f"Send 5: {acc.send(5)}")
print()


# Chaining generators with yield from
def chain_generators(*iterables):
    """Yield items from multiple iterables."""
    for iterable in iterables:
        yield from iterable


combined = chain_generators([1, 2, 3], ['a', 'b', 'c'], (10, 20))
print("Chained generators:", list(combined))
print()


# Practical example: reading large files line by line
def read_lines(filename):
    """Memory-efficient file reading."""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()


# This would be used like:
# for line in read_lines("large_file.txt"):
#     process(line)

print("Generators are perfect for processing large datasets!")

