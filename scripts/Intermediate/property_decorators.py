# This script demonstrates property decorators for getters, setters, and deleters
# Properties allow controlled access to instance attributes

# Basic property using @property decorator
class Circle:
    def __init__(self, radius):
        self._radius = radius  # Convention: underscore indicates "private"
    
    @property
    def radius(self):
        """Getter for radius."""
        print("Getting radius")
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Setter for radius with validation."""
        print(f"Setting radius to {value}")
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """Deleter for radius."""
        print("Deleting radius")
        del self._radius
    
    @property
    def diameter(self):
        """Read-only property - computed from radius."""
        return self._radius * 2
    
    @property
    def area(self):
        """Read-only property - computed area."""
        import math
        return math.pi * self._radius ** 2


# Using the Circle class
print("=== Basic Property Usage ===")
c = Circle(5)
print(f"Radius: {c.radius}")
print(f"Diameter: {c.diameter}")
print(f"Area: {c.area:.2f}")
print()

c.radius = 10  # Uses setter
print(f"New radius: {c.radius}")
print()


# Property for data validation
class Person:
    def __init__(self, name, age):
        self.name = name  # Uses setter
        self.age = age    # Uses setter
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 1:
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value
    
    @property
    def is_adult(self):
        """Computed property."""
        return self._age >= 18


print("=== Validation with Properties ===")
person = Person("  alice  ", 25)
print(f"Name: {person.name}")  # Automatically formatted
print(f"Age: {person.age}")
print(f"Is adult: {person.is_adult}")
print()


# Cached property (computed once, then stored)
class ExpensiveComputation:
    def __init__(self, data):
        self._data = data
        self._cached_result = None
    
    @property
    def result(self):
        """Expensive computation - cached after first access."""
        if self._cached_result is None:
            print("Computing expensive result...")
            import time
            time.sleep(0.1)  # Simulate expensive operation
            self._cached_result = sum(x**2 for x in self._data)
        return self._cached_result
    
    def clear_cache(self):
        """Clear the cached result."""
        self._cached_result = None


print("=== Cached Property ===")
comp = ExpensiveComputation([1, 2, 3, 4, 5])
print(f"First access: {comp.result}")  # Computes
print(f"Second access: {comp.result}")  # Uses cache
print()


# Using property() function directly (alternative to decorators)
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def get_width(self):
        return self._width
    
    def set_width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    # Create property using property() function
    width = property(get_width, set_width, doc="Rectangle width")
    
    # Same for height using lambda
    height = property(
        lambda self: self._height,
        lambda self, v: setattr(self, '_height', v) if v > 0 else (_ for _ in ()).throw(ValueError("Height must be positive")),
        doc="Rectangle height"
    )
    
    @property
    def area(self):
        return self._width * self._height


print("=== property() Function ===")
rect = Rectangle(5, 3)
print(f"Width: {rect.width}, Height: {rect.height}")
print(f"Area: {rect.area}")
rect.width = 10
print(f"New area: {rect.area}")
print()


# Properties with inheritance
class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
    
    @property
    def side(self):
        return self._width
    
    @side.setter
    def side(self, value):
        self._width = value
        self._height = value


print("=== Properties with Inheritance ===")
square = Square(4)
print(f"Side: {square.side}")
print(f"Area: {square.area}")
square.side = 6
print(f"New side: {square.side}, New area: {square.area}")
print()


# Using functools.cached_property (Python 3.8+)
from functools import cached_property


class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    @cached_property
    def statistics(self):
        """Computed once and cached automatically."""
        print("Computing statistics...")
        return {
            "sum": sum(self.data),
            "mean": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data),
        }


print("=== functools.cached_property ===")
analyzer = DataAnalyzer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"First access: {analyzer.statistics}")
print(f"Second access: {analyzer.statistics}")  # No recomputation

