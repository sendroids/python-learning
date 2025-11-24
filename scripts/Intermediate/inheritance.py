# This script demonstrates class inheritance and polymorphism
# Inheritance allows classes to inherit attributes and methods from parent classes

# Base class (parent)
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        raise NotImplementedError("Subclass must implement this method")
    
    def describe(self):
        return f"{self.name} is {self.age} years old"


# Derived classes (children)
class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # Call parent constructor
        self.breed = breed
    
    def speak(self):
        return f"{self.name} says Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball!"


class Cat(Animal):
    def __init__(self, name, age, indoor=True):
        super().__init__(name, age)
        self.indoor = indoor
    
    def speak(self):
        return f"{self.name} says Meow!"
    
    def scratch(self):
        return f"{self.name} is scratching the furniture!"


# Create instances
dog = Dog("Buddy", 5, "Golden Retriever")
cat = Cat("Whiskers", 3)

print(dog.describe())
print(dog.speak())
print(dog.fetch())
print(f"Breed: {dog.breed}")
print()

print(cat.describe())
print(cat.speak())
print(cat.scratch())
print(f"Indoor cat: {cat.indoor}")
print()


# Polymorphism - treating different objects uniformly
def animal_concert(animals):
    """Make all animals speak."""
    for animal in animals:
        print(animal.speak())


print("Animal Concert:")
animals = [Dog("Rex", 4, "German Shepherd"), Cat("Luna", 2), Dog("Max", 7, "Beagle")]
animal_concert(animals)
print()


# Multiple inheritance
class Flying:
    def fly(self):
        return f"{self.name} is flying!"


class Swimming:
    def swim(self):
        return f"{self.name} is swimming!"


class Duck(Animal, Flying, Swimming):
    def speak(self):
        return f"{self.name} says Quack!"


duck = Duck("Donald", 2)
print(duck.describe())
print(duck.speak())
print(duck.fly())
print(duck.swim())
print()


# Method Resolution Order (MRO)
print("Duck's Method Resolution Order:")
print(Duck.__mro__)
print()


# Using isinstance() and issubclass()
print(f"Is dog an Animal? {isinstance(dog, Animal)}")
print(f"Is dog a Dog? {isinstance(dog, Dog)}")
print(f"Is dog a Cat? {isinstance(dog, Cat)}")
print(f"Is Dog a subclass of Animal? {issubclass(Dog, Animal)}")
print()


# Abstract base classes
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


rect = Rectangle(5, 3)
circle = Circle(4)

print(f"Rectangle: area = {rect.area()}, perimeter = {rect.perimeter()}")
print(f"Circle: area = {circle.area():.2f}, perimeter = {circle.perimeter():.2f}")

