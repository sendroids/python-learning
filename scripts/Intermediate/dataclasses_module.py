# This script demonstrates dataclasses in Python
# Dataclasses reduce boilerplate code for classes that primarily store data

from dataclasses import dataclass, field, asdict, astuple
from typing import List, Optional

# Basic dataclass
@dataclass
class Point:
    x: float
    y: float


p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)

print("=== Basic Dataclass ===")
print(f"Point: {p1}")
print(f"Access attributes: x={p1.x}, y={p1.y}")
print(f"Equality check: p1 == p2 is {p1 == p2}")  # Automatic __eq__
print()


# Dataclass with default values
@dataclass
class Person:
    name: str
    age: int
    city: str = "Unknown"  # Default value


person1 = Person("Alice", 30)
person2 = Person("Bob", 25, "New York")

print("=== Default Values ===")
print(f"Person 1: {person1}")
print(f"Person 2: {person2}")
print()


# Dataclass with mutable default (use field())
@dataclass
class Team:
    name: str
    members: List[str] = field(default_factory=list)  # Mutable default
    score: int = field(default=0)
    _internal: str = field(default="private", repr=False)  # Hidden from repr


team = Team("Pythonistas")
team.members.append("Alice")
team.members.append("Bob")

print("=== Mutable Defaults with field() ===")
print(f"Team: {team}")
print(f"Members: {team.members}")
print()


# Frozen dataclass (immutable)
@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float


coord = Coordinate(40.7128, -74.0060)
print("=== Frozen (Immutable) Dataclass ===")
print(f"Coordinate: {coord}")
# coord.latitude = 0  # This would raise FrozenInstanceError
print(f"Hash (usable in sets/dicts): {hash(coord)}")
print()


# Dataclass with ordering
@dataclass(order=True)
class Student:
    sort_index: float = field(init=False, repr=False)
    name: str
    grade: float
    
    def __post_init__(self):
        # Set sort_index to grade for comparison
        self.sort_index = self.grade


students = [
    Student("Alice", 85.5),
    Student("Bob", 92.0),
    Student("Charlie", 78.0),
]

print("=== Ordered Dataclass ===")
print("Sorted by grade:")
for s in sorted(students, reverse=True):
    print(f"  {s}")
print()


# Using asdict() and astuple()
@dataclass
class Book:
    title: str
    author: str
    year: int
    pages: int


book = Book("Python Mastery", "John Doe", 2024, 350)

print("=== Conversion Utilities ===")
print(f"As dict: {asdict(book)}")
print(f"As tuple: {astuple(book)}")
print()


# Inheritance with dataclasses
@dataclass
class Animal:
    name: str
    age: int


@dataclass
class Dog(Animal):
    breed: str
    is_trained: bool = False


dog = Dog("Buddy", 5, "Golden Retriever", True)

print("=== Dataclass Inheritance ===")
print(f"Dog: {dog}")
print()


# Dataclass with computed fields using __post_init__
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    perimeter: float = field(init=False)
    
    def __post_init__(self):
        """Called after __init__ to compute derived values."""
        self.area = self.width * self.height
        self.perimeter = 2 * (self.width + self.height)


rect = Rectangle(5.0, 3.0)

print("=== Computed Fields with __post_init__ ===")
print(f"Rectangle: {rect}")
print()


# Dataclass with Optional and complex types
@dataclass
class Order:
    order_id: int
    customer: str
    items: List[str] = field(default_factory=list)
    discount: Optional[float] = None
    
    @property
    def item_count(self) -> int:
        return len(self.items)


order = Order(1001, "Alice", ["Book", "Pen", "Notebook"], 0.1)

print("=== Complex Dataclass ===")
print(f"Order: {order}")
print(f"Item count: {order.item_count}")
print()


# Comparing dataclass to regular class
print("=== Dataclass vs Regular Class ===")
print("Regular class needs __init__, __repr__, __eq__ manually.")
print("Dataclass generates them automatically!")

# This regular class is equivalent to the Point dataclass:
class PointRegular:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"PointRegular(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, PointRegular):
            return NotImplemented
        return self.x == other.x and self.y == other.y


# Slots for memory efficiency (Python 3.10+)
@dataclass(slots=True)
class EfficientPoint:
    x: float
    y: float


print("\n=== Memory Efficient with slots=True ===")
import sys
regular = Point(1.0, 2.0)
efficient = EfficientPoint(1.0, 2.0)
print(f"Regular Point size: {sys.getsizeof(regular.__dict__)} bytes (dict)")
print(f"Efficient Point: no __dict__, uses slots for memory efficiency")
print(f"EfficientPoint: {efficient}")

