# This script demonstrates magic/dunder methods in Python
# Magic methods have double underscores (dunder) and enable operator overloading

# Basic magic methods for string representation
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """Human-readable string (used by print())."""
        return f"Point at ({self.x}, {self.y})"
    
    def __repr__(self):
        """Developer-readable string (unambiguous)."""
        return f"Point({self.x}, {self.y})"


p = Point(3, 4)
print(f"str(p): {str(p)}")
print(f"repr(p): {repr(p)}")
print(f"print(p): {p}")
print()


# Comparison magic methods
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        """Equal to: =="""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age
    
    def __lt__(self, other):
        """Less than: <"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age
    
    def __le__(self, other):
        """Less than or equal: <="""
        return self == other or self < other
    
    def __gt__(self, other):
        """Greater than: >"""
        return not self <= other
    
    def __ge__(self, other):
        """Greater than or equal: >="""
        return not self < other
    
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


print("=== Comparison Methods ===")
alice = Person("Alice", 30)
bob = Person("Bob", 25)
charlie = Person("Charlie", 30)

print(f"alice == bob: {alice == bob}")
print(f"alice == charlie: {alice == charlie}")
print(f"alice > bob: {alice > bob}")
print(f"Sorted: {sorted([alice, bob, charlie])}")
print()


# Arithmetic magic methods
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Addition: +"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """Subtraction: -"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """Multiplication: * (vector * scalar)"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """Reverse multiplication: * (scalar * vector)"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        """Division: /"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x / scalar, self.y / scalar)
        return NotImplemented
    
    def __neg__(self):
        """Negation: -v"""
        return Vector(-self.x, -self.y)
    
    def __abs__(self):
        """Absolute value: abs(v) - returns magnitude"""
        return (self.x**2 + self.y**2) ** 0.5
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


print("=== Arithmetic Methods ===")
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"3 * v1 = {3 * v1}")
print(f"-v1 = {-v1}")
print(f"abs(v1) = {abs(v1)}")
print()


# Container magic methods
class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]
    
    def __len__(self):
        """Length: len(deck)"""
        return len(self.cards)
    
    def __getitem__(self, index):
        """Indexing: deck[i] or deck[i:j]"""
        return self.cards[index]
    
    def __setitem__(self, index, value):
        """Assignment: deck[i] = value"""
        self.cards[index] = value
    
    def __contains__(self, card):
        """Membership: card in deck"""
        return card in self.cards
    
    def __iter__(self):
        """Iteration: for card in deck"""
        return iter(self.cards)


print("=== Container Methods ===")
deck = Deck()
print(f"Deck length: {len(deck)}")
print(f"First card: {deck[0]}")
print(f"Last 3 cards: {deck[-3:]}")
print(f"'Ace of Spades' in deck: {'A of Spades' in deck}")
print()


# Callable objects with __call__
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, value):
        """Make object callable like a function."""
        return value * self.factor


print("=== Callable Objects ===")
double = Multiplier(2)
triple = Multiplier(3)

print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")
print()


# Context manager magic methods
class Timer:
    def __enter__(self):
        """Called when entering 'with' block."""
        import time
        self.start = time.time()
        print("Timer started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block."""
        import time
        elapsed = time.time() - self.start
        print(f"Timer stopped: {elapsed:.4f} seconds")
        return False  # Don't suppress exceptions


print("=== Context Manager Methods ===")
with Timer():
    import time
    time.sleep(0.1)
print()


# Hash and equality for use in sets/dicts
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)
    
    def __hash__(self):
        """Required for use in sets/dicts."""
        return hash((self.r, self.g, self.b))
    
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"


print("=== Hash Method ===")
colors = {Color(255, 0, 0): "red", Color(0, 255, 0): "green"}
print(f"Color dict: {colors}")
print(f"Lookup: {colors[Color(255, 0, 0)]}")

color_set = {Color(255, 0, 0), Color(0, 255, 0), Color(255, 0, 0)}
print(f"Color set (duplicates removed): {color_set}")

