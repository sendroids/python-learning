# This script demonstrates descriptors in Python
# Descriptors are the mechanism behind properties, methods, and attribute access

from typing import Any, Type, Optional, Callable, TypeVar, Generic
from weakref import WeakKeyDictionary

print("=== Understanding Descriptors ===")
print("Descriptors control attribute access via __get__, __set__, __delete__")
print()


# Basic descriptor example
class SimpleDescriptor:
    """A simple descriptor that stores values per-instance."""
    
    def __set_name__(self, owner: Type, name: str) -> None:
        """Called when descriptor is assigned to a class attribute."""
        self.name = name
        self.private_name = f'_desc_{name}'
        print(f"Descriptor '{name}' bound to class '{owner.__name__}'")
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        """Called when attribute is accessed."""
        if obj is None:
            # Accessed via class, return descriptor itself
            return self
        value = getattr(obj, self.private_name, None)
        print(f"Getting {self.name}: {value}")
        return value
    
    def __set__(self, obj: Any, value: Any) -> None:
        """Called when attribute is set."""
        print(f"Setting {self.name} to {value}")
        setattr(obj, self.private_name, value)
    
    def __delete__(self, obj: Any) -> None:
        """Called when attribute is deleted."""
        print(f"Deleting {self.name}")
        delattr(obj, self.private_name)


class MyClass:
    value = SimpleDescriptor()


print("=== Basic Descriptor Demo ===")
obj = MyClass()
obj.value = 42
print(f"obj.value = {obj.value}")
print()


# Data descriptor vs Non-data descriptor
print("=== Data vs Non-Data Descriptors ===")


class DataDescriptor:
    """Data descriptor: defines __get__ AND __set__ (or __delete__)."""
    
    def __get__(self, obj, objtype=None):
        return "Data descriptor value"
    
    def __set__(self, obj, value):
        pass  # Even empty __set__ makes it a data descriptor


class NonDataDescriptor:
    """Non-data descriptor: only defines __get__."""
    
    def __get__(self, obj, objtype=None):
        return "Non-data descriptor value"


class Example:
    data = DataDescriptor()
    nondata = NonDataDescriptor()


e = Example()
e.__dict__['data'] = "Instance data"      # Won't override data descriptor
e.__dict__['nondata'] = "Instance nondata"  # WILL override non-data descriptor

print(f"e.data: {e.data}")       # Data descriptor wins
print(f"e.nondata: {e.nondata}")  # Instance dict wins
print("Lookup order: Data descriptor > Instance dict > Non-data descriptor > Class dict")
print()


# Validated descriptor
print("=== Validation Descriptors ===")


class Validated:
    """Base class for validated descriptors."""
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.private_name = f'_validated_{name}'
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj: Any, value: Any) -> None:
        self.validate(value)
        setattr(obj, self.private_name, value)
    
    def validate(self, value: Any) -> None:
        """Override in subclasses to add validation."""
        pass


class PositiveNumber(Validated):
    """Descriptor that only accepts positive numbers."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")


class NonEmptyString(Validated):
    """Descriptor that only accepts non-empty strings."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if not value.strip():
            raise ValueError(f"{self.name} cannot be empty")


class RangeValidator(Validated):
    """Descriptor with configurable range validation."""
    
    def __init__(self, min_val: float, max_val: float) -> None:
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if not self.min_val <= value <= self.max_val:
            raise ValueError(
                f"{self.name} must be between {self.min_val} and {self.max_val}"
            )


class Product:
    """Product with validated attributes."""
    name = NonEmptyString()
    price = PositiveNumber()
    quantity = RangeValidator(0, 1000)


product = Product()
product.name = "Widget"
product.price = 19.99
product.quantity = 100

print(f"Product: {product.name}, ${product.price}, qty: {product.quantity}")

try:
    product.price = -5
except ValueError as e:
    print(f"Validation error: {e}")

try:
    product.name = "   "
except ValueError as e:
    print(f"Validation error: {e}")
print()


# Type-checked descriptor with generics
print("=== Type-Checked Descriptor ===")

T = TypeVar('T')


class TypeChecked(Generic[T]):
    """Generic descriptor that enforces a specific type."""
    
    def __init__(self, expected_type: Type[T]) -> None:
        self.expected_type = expected_type
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.private_name = f'_typed_{name}'
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Optional[T]:
        if obj is None:
            return self  # type: ignore
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj: Any, value: T) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, self.private_name, value)


class Person:
    name = TypeChecked(str)
    age = TypeChecked(int)
    active = TypeChecked(bool)


person = Person()
person.name = "Alice"
person.age = 30
person.active = True
print(f"Person: {person.name}, age {person.age}, active: {person.active}")

try:
    person.age = "thirty"  # type: ignore
except TypeError as e:
    print(f"Type error: {e}")
print()


# Cached/Lazy descriptor
print("=== Lazy/Cached Property Descriptor ===")


class LazyProperty:
    """Descriptor that computes value once and caches it."""
    
    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        
        # Compute and cache the value
        value = self.func(obj)
        # Replace descriptor with computed value in instance __dict__
        obj.__dict__[self.name] = value
        print(f"Computed and cached {self.name}")
        return value


class DataAnalyzer:
    def __init__(self, data: list[int]) -> None:
        self.data = data
    
    @LazyProperty
    def statistics(self) -> dict:
        """Expensive computation done only once."""
        print("Computing statistics...")
        return {
            'mean': sum(self.data) / len(self.data),
            'min': min(self.data),
            'max': max(self.data),
            'sum': sum(self.data),
        }


analyzer = DataAnalyzer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("First access:")
print(f"  Stats: {analyzer.statistics}")
print("Second access (cached):")
print(f"  Stats: {analyzer.statistics}")
print()


# Descriptor with instance-level storage using WeakKeyDictionary
print("=== Descriptor with WeakKeyDictionary Storage ===")


class WeakDescriptor:
    """Descriptor that uses WeakKeyDictionary for memory-safe storage."""
    
    def __init__(self, default: Any = None) -> None:
        self.default = default
        self.data: WeakKeyDictionary = WeakKeyDictionary()
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        return self.data.get(obj, self.default)
    
    def __set__(self, obj: Any, value: Any) -> None:
        self.data[obj] = value
    
    def __delete__(self, obj: Any) -> None:
        if obj in self.data:
            del self.data[obj]


class Session:
    user_id = WeakDescriptor(default="anonymous")
    token = WeakDescriptor()


s1 = Session()
s2 = Session()
s1.user_id = "user_123"
s1.token = "abc123"
s2.user_id = "user_456"

print(f"Session 1: {s1.user_id}, token: {s1.token}")
print(f"Session 2: {s2.user_id}, token: {s2.token}")
print("(When instances are garbage collected, their data is automatically cleaned)")
print()


# Read-only descriptor
print("=== Read-Only Descriptor ===")


class ReadOnly:
    """Descriptor for read-only attributes that can only be set once."""
    
    def __init__(self, initial_value: Any = None) -> None:
        self.initial_value = initial_value
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.private_name = f'_readonly_{name}'
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self.private_name, self.initial_value)
    
    def __set__(self, obj: Any, value: Any) -> None:
        if hasattr(obj, self.private_name):
            raise AttributeError(f"{self.name} is read-only")
        setattr(obj, self.private_name, value)


class Entity:
    id = ReadOnly()
    
    def __init__(self, entity_id: int) -> None:
        self.id = entity_id


entity = Entity(42)
print(f"Entity ID: {entity.id}")

try:
    entity.id = 100  # Attempt to modify
except AttributeError as e:
    print(f"Read-only error: {e}")
print()


# Delegating descriptor
print("=== Delegating Descriptor ===")


class Delegator:
    """Descriptor that delegates to another object's attribute."""
    
    def __init__(self, delegate_attr: str, target_attr: str) -> None:
        self.delegate_attr = delegate_attr
        self.target_attr = target_attr
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        delegate = getattr(obj, self.delegate_attr)
        return getattr(delegate, self.target_attr)
    
    def __set__(self, obj: Any, value: Any) -> None:
        delegate = getattr(obj, self.delegate_attr)
        setattr(delegate, self.target_attr, value)


class Address:
    def __init__(self, street: str, city: str) -> None:
        self.street = street
        self.city = city


class Customer:
    # Delegate to _address object
    street = Delegator('_address', 'street')
    city = Delegator('_address', 'city')
    
    def __init__(self, name: str, address: Address) -> None:
        self.name = name
        self._address = address


addr = Address("123 Main St", "Boston")
customer = Customer("Alice", addr)

print(f"Customer: {customer.name}")
print(f"Street (delegated): {customer.street}")
print(f"City (delegated): {customer.city}")

customer.city = "New York"  # Modifies the underlying Address
print(f"Updated city: {customer.city}")
print(f"Address city: {addr.city}")  # Same object was modified
print()


# Observable descriptor (observer pattern)
print("=== Observable Descriptor ===")


class Observable:
    """Descriptor that notifies callbacks when value changes."""
    
    def __init__(self, initial: Any = None) -> None:
        self.initial = initial
        self.callbacks: list[Callable] = []
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.private_name = f'_observable_{name}'
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self.private_name, self.initial)
    
    def __set__(self, obj: Any, value: Any) -> None:
        old_value = getattr(obj, self.private_name, self.initial)
        setattr(obj, self.private_name, value)
        
        # Notify all callbacks
        for callback in self.callbacks:
            callback(obj, self.name, old_value, value)
    
    def add_callback(self, callback: Callable) -> None:
        self.callbacks.append(callback)


class Model:
    status = Observable("pending")


def on_status_change(obj, name, old, new):
    print(f"  Status changed: {old} -> {new}")


Model.status.add_callback(on_status_change)

model = Model()
model.status = "processing"
model.status = "completed"
print()


# How properties work (simplified implementation)
print("=== How Properties Work (Behind the Scenes) ===")


class Property:
    """Simplified implementation of the built-in property descriptor."""
    
    def __init__(
        self,
        fget: Optional[Callable] = None,
        fset: Optional[Callable] = None,
        fdel: Optional[Callable] = None,
        doc: Optional[str] = None
    ) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget.__doc__ if fget else None)
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Any:
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    
    def __set__(self, obj: Any, value: Any) -> None:
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
    
    def __delete__(self, obj: Any) -> None:
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    
    def getter(self, fget: Callable) -> 'Property':
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset: Callable) -> 'Property':
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel: Callable) -> 'Property':
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius
    
    @Property
    def radius(self) -> float:
        """The radius of the circle."""
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value


circle = Circle(5.0)
print(f"Circle radius: {circle.radius}")
circle.radius = 10.0
print(f"Updated radius: {circle.radius}")
print()


# Method as descriptor
print("=== Methods as Descriptors ===")


class Method:
    """Simplified implementation showing how methods are descriptors."""
    
    def __init__(self, func: Callable) -> None:
        self.func = func
    
    def __get__(self, obj: Any, objtype: Optional[Type] = None) -> Callable:
        if obj is None:
            # Unbound method (accessed via class)
            return self.func
        # Bound method (accessed via instance)
        def bound_method(*args, **kwargs):
            return self.func(obj, *args, **kwargs)
        return bound_method


class Demo:
    @Method
    def greet(self, name: str) -> str:
        return f"Hello, {name}! (from {self})"


demo = Demo()
print(f"Calling bound method: {demo.greet('World')}")
print(f"Unbound function: {Demo.greet}")
print()


print("=== Key Takeaways ===")
print("1. Descriptors use __get__, __set__, __delete__ to control attribute access")
print("2. Data descriptors (with __set__) take precedence over instance __dict__")
print("3. Non-data descriptors (only __get__) can be overridden by instance attributes")
print("4. __set_name__ is called when descriptor is assigned to class attribute")
print("5. Properties, methods, classmethod, staticmethod are all descriptors")
print("6. Use descriptors for: validation, lazy evaluation, delegation, caching")
print("7. WeakKeyDictionary prevents memory leaks with instance-level storage")

