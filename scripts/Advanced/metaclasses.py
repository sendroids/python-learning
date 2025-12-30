# This script demonstrates metaclasses in Python
# Metaclasses are "classes of classes" - they control how classes are created

# Understanding the type hierarchy
print("=== Understanding type() and Metaclasses ===")

# Everything in Python is an object, including classes
class MyClass:
    pass

obj = MyClass()

print(f"obj is instance of MyClass: {isinstance(obj, MyClass)}")
print(f"MyClass is instance of type: {isinstance(MyClass, type)}")
print(f"type of obj: {type(obj)}")
print(f"type of MyClass: {type(MyClass)}")
print(f"type of type: {type(type)}")  # type is its own metaclass!
print()


# Creating a class dynamically with type()
print("=== Creating Classes Dynamically with type() ===")

# type(name, bases, attrs) creates a new class
DynamicClass = type(
    'DynamicClass',  # Class name
    (object,),       # Base classes (tuple)
    {                # Class attributes and methods
        'x': 10,
        'greet': lambda self: f"Hello from {self.__class__.__name__}!",
    }
)

instance = DynamicClass()
print(f"Dynamic class: {DynamicClass}")
print(f"instance.x: {instance.x}")
print(f"instance.greet(): {instance.greet()}")
print()


# Basic custom metaclass
print("=== Basic Custom Metaclass ===")

class MyMeta(type):
    """A simple metaclass that prints when classes are created."""
    
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        print(f"Bases: {bases}")
        print(f"Namespace keys: {list(namespace.keys())}")
        # Call type.__new__ to actually create the class
        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class MyTrackedClass(metaclass=MyMeta):
    """This class uses MyMeta as its metaclass."""
    class_attr = "I'm a class attribute"
    
    def method(self):
        return "I'm a method"


print(f"Type of MyTrackedClass: {type(MyTrackedClass)}")
print()


# Metaclass that modifies class creation
print("=== Metaclass That Modifies Classes ===")

class AutoPropertyMeta(type):
    """Metaclass that automatically creates properties from _private attributes."""
    
    def __new__(mcs, name, bases, namespace):
        # Find all _private attributes and create properties for them
        new_namespace = dict(namespace)
        
        for key, value in list(namespace.items()):
            if key.startswith('_') and not key.startswith('__'):
                prop_name = key[1:]  # Remove leading underscore
                
                # Create getter
                def make_getter(attr_name):
                    def getter(self):
                        return getattr(self, attr_name)
                    return getter
                
                # Create setter
                def make_setter(attr_name):
                    def setter(self, value):
                        setattr(self, attr_name, value)
                    return setter
                
                new_namespace[prop_name] = property(
                    make_getter(key),
                    make_setter(key)
                )
        
        return super().__new__(mcs, name, bases, new_namespace)


class Person(metaclass=AutoPropertyMeta):
    _name = "Unknown"
    _age = 0
    
    def __init__(self, name, age):
        self._name = name
        self._age = age


p = Person("Alice", 30)
print(f"Using auto-generated property: p.name = {p.name}")
print(f"Using auto-generated property: p.age = {p.age}")
p.name = "Bob"  # Using the setter
print(f"After setting: p.name = {p.name}")
print()


# Singleton pattern with metaclass
print("=== Singleton Pattern with Metaclass ===")

class SingletonMeta(type):
    """Metaclass that ensures only one instance of a class exists."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # First time: create the instance
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """A singleton database connection class."""
    
    def __init__(self, connection_string="default"):
        self.connection_string = connection_string
        print(f"Initializing Database with: {connection_string}")
    
    def query(self, sql):
        return f"Executing on {self.connection_string}: {sql}"


# Both variables reference the same instance
db1 = Database("postgresql://localhost/db1")
db2 = Database("mysql://localhost/db2")  # __init__ not called again!

print(f"db1 is db2: {db1 is db2}")
print(f"Connection string: {db1.connection_string}")  # Still the first one
print()


# Registry pattern with metaclass
print("=== Registry Pattern with Metaclass ===")

class PluginRegistry(type):
    """Metaclass that automatically registers all subclasses."""
    
    plugins = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself
        if bases != (object,) and bases:
            mcs.plugins[name.lower()] = cls
        return cls
    
    @classmethod
    def get_plugin(mcs, name):
        return mcs.plugins.get(name.lower())
    
    @classmethod
    def list_plugins(mcs):
        return list(mcs.plugins.keys())


class BasePlugin(metaclass=PluginRegistry):
    """Base class for all plugins."""
    def execute(self):
        raise NotImplementedError


class JSONPlugin(BasePlugin):
    """Plugin for JSON processing."""
    def execute(self):
        return "Processing JSON"


class XMLPlugin(BasePlugin):
    """Plugin for XML processing."""
    def execute(self):
        return "Processing XML"


class CSVPlugin(BasePlugin):
    """Plugin for CSV processing."""
    def execute(self):
        return "Processing CSV"


print(f"Registered plugins: {PluginRegistry.list_plugins()}")
plugin_cls = PluginRegistry.get_plugin('jsonplugin')
print(f"Got plugin: {plugin_cls}")
print(f"Execute: {plugin_cls().execute()}")
print()


# Validation metaclass
print("=== Validation Metaclass ===")

class ValidatedMeta(type):
    """Metaclass that validates class definitions."""
    
    def __new__(mcs, name, bases, namespace):
        # Skip validation for the base class
        if bases:
            # Require docstring
            if not namespace.get('__doc__'):
                raise TypeError(f"Class {name} must have a docstring")
            
            # Require certain methods
            required_methods = getattr(bases[0], '__required_methods__', [])
            for method in required_methods:
                if method not in namespace:
                    raise TypeError(f"Class {name} must implement {method}()")
        
        return super().__new__(mcs, name, bases, namespace)


class Validator(metaclass=ValidatedMeta):
    """Base validator class."""
    __required_methods__ = ['validate']


class EmailValidator(Validator):
    """Validates email addresses."""
    
    def validate(self, value):
        return '@' in value and '.' in value


# This would raise TypeError:
# class BrokenValidator(Validator):
#     """Missing validate method."""
#     pass

validator = EmailValidator()
print(f"Validating 'test@example.com': {validator.validate('test@example.com')}")
print(f"Validating 'invalid': {validator.validate('invalid')}")
print()


# Metaclass with __init__ and __call__
print("=== Metaclass __init__ and __call__ ===")

class LoggingMeta(type):
    """Metaclass that logs class creation and instantiation."""
    
    def __init__(cls, name, bases, namespace):
        print(f"[META __init__] Initializing class: {name}")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        print(f"[META __call__] Creating instance of: {cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        print(f"[META __call__] Instance created: {instance}")
        return instance


class LoggedClass(metaclass=LoggingMeta):
    def __init__(self, value):
        print(f"[CLASS __init__] Setting value: {value}")
        self.value = value


print("\nCreating instance:")
obj = LoggedClass(42)
print()


# Abstract Base Class behavior with metaclass
print("=== ABC-like Behavior with Metaclass ===")

class AbstractMeta(type):
    """Metaclass that enforces abstract method implementation."""
    
    def __call__(cls, *args, **kwargs):
        # Check for unimplemented abstract methods
        abstract_methods = getattr(cls, '__abstract_methods__', set())
        if abstract_methods:
            raise TypeError(
                f"Can't instantiate {cls.__name__} with abstract methods: "
                f"{', '.join(abstract_methods)}"
            )
        return super().__call__(*args, **kwargs)


def abstractmethod(func):
    """Decorator to mark a method as abstract."""
    func.__isabstract__ = True
    return func


class AbstractBase(metaclass=AbstractMeta):
    """Base class with abstract method support."""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Collect abstract methods from parent classes
        abstract = set()
        for base in cls.__mro__:
            for name, value in vars(base).items():
                if getattr(value, '__isabstract__', False):
                    abstract.add(name)
        
        # Remove methods that are implemented in this class
        for name in list(abstract):
            if name in vars(cls) and not getattr(vars(cls)[name], '__isabstract__', False):
                abstract.discard(name)
        
        cls.__abstract_methods__ = abstract


class Shape(AbstractBase):
    """Abstract shape class."""
    
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass


class Rectangle(Shape):
    """Concrete rectangle implementation."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


rect = Rectangle(5, 3)
print(f"Rectangle area: {rect.area()}")
print(f"Rectangle perimeter: {rect.perimeter()}")

# This would raise TypeError:
# shape = Shape()  # Can't instantiate with abstract methods
print()


# __prepare__ for custom namespace
print("=== __prepare__ for Custom Namespace ===")

from collections import OrderedDict

class OrderedMeta(type):
    """Metaclass that tracks the order of attribute definitions."""
    
    @classmethod
    def __prepare__(mcs, name, bases):
        # Return a custom namespace (must be a mapping)
        return OrderedDict()
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, dict(namespace))
        # Store the original order of definitions
        cls._field_order = [
            key for key in namespace.keys()
            if not key.startswith('_')
        ]
        return cls


class OrderedFields(metaclass=OrderedMeta):
    first = 1
    second = 2
    third = 3
    fourth = 4


print(f"Field order: {OrderedFields._field_order}")
print()


print("=== Key Takeaways ===")
print("1. Metaclasses control class creation (class of a class)")
print("2. type() is the default metaclass for all classes")
print("3. Use __new__ to modify class before creation")
print("4. Use __init__ to configure class after creation")
print("5. Use __call__ to control instantiation")
print("6. Common patterns: Singleton, Registry, Validation")
print("7. Consider simpler alternatives: decorators, __init_subclass__")

