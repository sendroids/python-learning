# This script demonstrates the collections module
# Collections provides specialized container datatypes

from collections import Counter, defaultdict, namedtuple, deque, OrderedDict, ChainMap

# Counter - count hashable objects
print("=== Counter ===")
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_counts = Counter(words)

print(f"Word counts: {word_counts}")
print(f"Most common 2: {word_counts.most_common(2)}")
print(f"Count of 'apple': {word_counts['apple']}")

# Counter with strings
text = "mississippi"
char_counts = Counter(text)
print(f"Character counts in '{text}': {char_counts}")

# Counter arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(f"Counter addition: {c1 + c2}")
print(f"Counter subtraction: {c1 - c2}")
print()


# defaultdict - dict with default factory
print("=== defaultdict ===")
# Regular dict raises KeyError for missing keys
# defaultdict creates default values automatically

# Group words by first letter
words = ["apple", "ant", "banana", "bear", "cherry", "cat"]
grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)

print(f"Words grouped by first letter: {dict(grouped)}")

# Count with defaultdict
counts = defaultdict(int)
for word in words:
    counts[word] += 1
print(f"Word counts: {dict(counts)}")

# Nested defaultdict
nested = defaultdict(lambda: defaultdict(list))
nested["fruits"]["red"].append("apple")
nested["fruits"]["yellow"].append("banana")
print(f"Nested structure: {dict(nested)}")
print()


# namedtuple - tuple with named fields
print("=== namedtuple ===")
Point = namedtuple("Point", ["x", "y"])
p1 = Point(3, 4)
p2 = Point(x=1, y=2)

print(f"Point p1: {p1}")
print(f"Access by name: x={p1.x}, y={p1.y}")
print(f"Access by index: x={p1[0]}, y={p1[1]}")
print(f"As dict: {p1._asdict()}")

# Create new point with modified field
p3 = p1._replace(x=10)
print(f"Modified point: {p3}")

# Practical example: representing data
Person = namedtuple("Person", ["name", "age", "city"])
people = [
    Person("Alice", 30, "New York"),
    Person("Bob", 25, "Los Angeles"),
    Person("Charlie", 35, "Chicago"),
]

for person in people:
    print(f"  {person.name}, {person.age}, from {person.city}")
print()


# deque - double-ended queue
print("=== deque ===")
d = deque([1, 2, 3])

# Add to both ends
d.append(4)        # Add to right
d.appendleft(0)    # Add to left
print(f"After appending: {d}")

# Remove from both ends
d.pop()            # Remove from right
d.popleft()        # Remove from left
print(f"After popping: {d}")

# Rotate elements
d = deque([1, 2, 3, 4, 5])
d.rotate(2)        # Rotate right
print(f"After rotate(2): {d}")
d.rotate(-2)       # Rotate left
print(f"After rotate(-2): {d}")

# Max length deque (oldest items removed automatically)
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(f"  Added {i}: {list(recent)}")
print()


# OrderedDict - dict that remembers insertion order
print("=== OrderedDict ===")
# Note: Regular dicts maintain order in Python 3.7+, but OrderedDict has extra features

od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3

print(f"OrderedDict: {od}")

# Move to end
od.move_to_end("first")
print(f"After move_to_end('first'): {od}")

# Move to beginning
od.move_to_end("third", last=False)
print(f"After move_to_end('third', last=False): {od}")
print()


# ChainMap - combine multiple dicts
print("=== ChainMap ===")
defaults = {"color": "red", "size": "medium", "theme": "light"}
user_settings = {"color": "blue"}
temp_settings = {"size": "large"}

settings = ChainMap(temp_settings, user_settings, defaults)

print(f"Combined settings: {dict(settings)}")
print(f"Color (user override): {settings['color']}")
print(f"Size (temp override): {settings['size']}")
print(f"Theme (default): {settings['theme']}")

# Maps attribute shows all dicts in chain
print(f"All maps: {settings.maps}")

