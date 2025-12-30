# This script demonstrates advanced type hints and the typing module
# Type hints enable better IDE support, documentation, and static analysis

from typing import (
    TypeVar, Generic, Protocol, Callable, Literal, Final,
    Union, Optional, Any, overload, ClassVar, cast,
    Sequence, Mapping, MutableMapping, Iterable, Iterator,
    Tuple, List, Dict, Set, FrozenSet,
    get_type_hints, get_origin, get_args,
    NamedTuple, TypedDict, Annotated
)
from abc import abstractmethod
from dataclasses import dataclass
import sys

print("=== TypeVar: Generic Type Variables ===")

# TypeVar creates a type variable for generics
T = TypeVar('T')  # Can be any type
Number = TypeVar('Number', int, float)  # Constrained to int or float
Comparable = TypeVar('Comparable', bound='SupportsLessThan')  # Bounded


def first_element(items: list[T]) -> T:
    """Return first element, preserving the type."""
    return items[0]


# The type checker knows the return types
int_result: int = first_element([1, 2, 3])
str_result: str = first_element(["a", "b", "c"])
print(f"First int: {int_result}, First str: {str_result}")


def add_numbers(a: Number, b: Number) -> Number:
    """Add two numbers of the same numeric type."""
    return a + b


print(f"add_numbers(1, 2) = {add_numbers(1, 2)}")
print(f"add_numbers(1.5, 2.5) = {add_numbers(1.5, 2.5)}")
print()


print("=== Generic Classes ===")

# Creating generic classes
class Stack(Generic[T]):
    """A generic stack implementation."""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]
    
    def __len__(self) -> int:
        return len(self._items)


# Type-safe stacks
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"Int stack peek: {int_stack.peek()}")

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
print(f"String stack pop: {str_stack.pop()}")
print()


# Multiple type parameters
K = TypeVar('K')
V = TypeVar('V')


class Pair(Generic[K, V]):
    """A generic pair/tuple class."""
    
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
    
    def swap(self) -> 'Pair[V, K]':
        return Pair(self.value, self.key)


pair: Pair[str, int] = Pair("age", 30)
print(f"Pair: ({pair.key}, {pair.value})")
swapped: Pair[int, str] = pair.swap()
print(f"Swapped: ({swapped.key}, {swapped.value})")
print()


print("=== Protocols: Structural Subtyping (Duck Typing) ===")


class SupportsLessThan(Protocol):
    """Protocol for objects that support < comparison."""
    
    def __lt__(self, other: Any) -> bool: ...


class SupportsClose(Protocol):
    """Protocol for objects with a close method."""
    
    def close(self) -> None: ...


class Drawable(Protocol):
    """Protocol for drawable objects."""
    
    def draw(self) -> str: ...
    
    @property
    def visible(self) -> bool: ...


# This class implements Drawable without inheriting
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius
        self._visible = True
    
    def draw(self) -> str:
        return f"○ (radius: {self.radius})"
    
    @property
    def visible(self) -> bool:
        return self._visible


class Square:
    def __init__(self, side: float) -> None:
        self.side = side
        self._visible = True
    
    def draw(self) -> str:
        return f"□ (side: {self.side})"
    
    @property
    def visible(self) -> bool:
        return self._visible


def render(shapes: list[Drawable]) -> None:
    """Render all drawable shapes."""
    for shape in shapes:
        if shape.visible:
            print(f"  Rendering: {shape.draw()}")


shapes: list[Drawable] = [Circle(5.0), Square(3.0)]
print("Rendering shapes:")
render(shapes)
print()


# Runtime checkable protocol
from typing import runtime_checkable


@runtime_checkable
class Closeable(Protocol):
    """Runtime-checkable protocol for closeable objects."""
    
    def close(self) -> None: ...


class FileWrapper:
    def close(self) -> None:
        print("Closing file")


class Connection:
    def close(self) -> None:
        print("Closing connection")


fw = FileWrapper()
print(f"FileWrapper is Closeable: {isinstance(fw, Closeable)}")
print(f"str is Closeable: {isinstance('hello', Closeable)}")
print()


print("=== Callable Types ===")


# Function type hints
def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    """Apply a binary operation to two integers."""
    return operation(x, y)


print(f"apply_operation(5, 3, lambda a, b: a + b) = {apply_operation(5, 3, lambda a, b: a + b)}")
print(f"apply_operation(5, 3, lambda a, b: a * b) = {apply_operation(5, 3, lambda a, b: a * b)}")


# Callable with variable arguments
Handler = Callable[..., None]  # Any args, returns None


def register_handler(handler: Handler) -> None:
    """Register a handler function."""
    print(f"Registered: {handler.__name__}")


def my_handler(event: str, data: dict) -> None:
    pass


register_handler(my_handler)
print()


print("=== Literal Types ===")


def set_mode(mode: Literal["read", "write", "append"]) -> str:
    """Set file mode - only specific strings allowed."""
    return f"Mode set to: {mode}"


print(set_mode("read"))
print(set_mode("write"))
# set_mode("invalid")  # Type checker would flag this


# Literal with other types
def get_status_code() -> Literal[200, 404, 500]:
    """Return one of the predefined status codes."""
    return 200


print(f"Status code: {get_status_code()}")
print()


print("=== Final and ClassVar ===")

# Final: value cannot be reassigned
MAX_SIZE: Final[int] = 100
API_VERSION: Final = "1.0.0"  # Type inferred

print(f"MAX_SIZE: {MAX_SIZE}")
print(f"API_VERSION: {API_VERSION}")


class Config:
    """Configuration with class variables and final values."""
    
    # ClassVar: belongs to class, not instances
    instances: ClassVar[int] = 0
    default_timeout: ClassVar[float] = 30.0
    
    # Final: cannot be overridden in subclasses
    VERSION: Final = "2.0"
    
    def __init__(self, name: str) -> None:
        Config.instances += 1
        self.name = name


c1 = Config("first")
c2 = Config("second")
print(f"Config instances: {Config.instances}")
print(f"Config VERSION: {Config.VERSION}")
print()


print("=== Function Overloading ===")


@overload
def process(value: int) -> str: ...

@overload
def process(value: str) -> int: ...

@overload
def process(value: list[int]) -> int: ...


def process(value: int | str | list[int]) -> str | int:
    """Process different types of input."""
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return sum(value)
    raise TypeError(f"Unsupported type: {type(value)}")


# Type checker knows the exact return type for each call
str_val: str = process(42)
int_val: int = process("hello")
sum_val: int = process([1, 2, 3])

print(f"process(42) -> '{str_val}' (str)")
print(f"process('hello') -> {int_val} (int)")
print(f"process([1,2,3]) -> {sum_val} (int)")
print()


print("=== TypedDict: Typed Dictionaries ===")


class MovieDict(TypedDict):
    """A dictionary with specific string keys and typed values."""
    title: str
    year: int
    rating: float


class MovieDictPartial(TypedDict, total=False):
    """All keys are optional."""
    title: str
    year: int
    rating: float


def display_movie(movie: MovieDict) -> None:
    """Display movie information."""
    print(f"  {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")


movie: MovieDict = {
    "title": "Inception",
    "year": 2010,
    "rating": 8.8
}
display_movie(movie)
print()


print("=== NamedTuple with Types ===")


class Point(NamedTuple):
    """A 2D point with named, typed fields."""
    x: float
    y: float
    label: str = "origin"  # Default value


class Color(NamedTuple):
    """RGB color."""
    red: int
    green: int
    blue: int


p = Point(3.0, 4.0, "A")
c = Color(255, 128, 0)

print(f"Point: {p}, x={p.x}, y={p.y}")
print(f"Color: {c}, red={c.red}")
print()


print("=== Annotated: Metadata in Type Hints ===")


# Annotated allows adding metadata to type hints
Width = Annotated[int, "width in pixels", lambda x: x > 0]
Height = Annotated[int, "height in pixels", lambda x: x > 0]


@dataclass
class Image:
    """Image with annotated dimensions."""
    width: Annotated[int, "Width must be positive"]
    height: Annotated[int, "Height must be positive"]
    format: Annotated[str, Literal["png", "jpg", "gif"]]


img = Image(1920, 1080, "png")
print(f"Image: {img.width}x{img.height} ({img.format})")

# Get metadata from annotations
hints = get_type_hints(Image, include_extras=True)
print(f"Width annotation: {hints['width']}")
print()


print("=== Type Introspection ===")


def analyze_type(hint: Any) -> None:
    """Analyze a type hint."""
    print(f"Type: {hint}")
    print(f"  Origin: {get_origin(hint)}")
    print(f"  Args: {get_args(hint)}")


print("Analyzing generic types:")
analyze_type(list[int])
analyze_type(dict[str, int])
analyze_type(Optional[str])  # Same as Union[str, None]
print()


print("=== Type Guards (Python 3.10+) ===")

from typing import TypeGuard


def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """Type guard that checks if all elements are strings."""
    return all(isinstance(x, str) for x in val)


def process_strings(items: list[Any]) -> None:
    """Process items, with type narrowing."""
    if is_string_list(items):
        # Type checker knows items is list[str] here
        for item in items:
            print(f"  String: {item.upper()}")
    else:
        print("  Not all strings!")


process_strings(["hello", "world"])
process_strings(["hello", 42])
print()


print("=== ParamSpec: Preserving Function Signatures ===")

from typing import ParamSpec, Concatenate

P = ParamSpec('P')
R = TypeVar('R')


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that preserves the function signature."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_call
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


# Type checker knows greet still has (name: str, greeting: str) -> str
result = greet("Alice", greeting="Hi")
print(f"Result: {result}")
print()


print("=== Self Type (Python 3.11+) ===")

# For older versions, we can simulate Self
from typing import TypeVar
Self = TypeVar('Self', bound='Builder')


class Builder:
    """Fluent builder pattern with proper typing."""
    
    def __init__(self) -> None:
        self._parts: list[str] = []
    
    def add(self: Self, part: str) -> Self:
        """Add a part and return self for chaining."""
        self._parts.append(part)
        return self
    
    def build(self) -> str:
        return " | ".join(self._parts)


class AdvancedBuilder(Builder):
    def add_special(self: Self, part: str) -> Self:
        return self.add(f"*{part}*")


# Chaining works with correct types
result = (
    AdvancedBuilder()
    .add("first")
    .add_special("special")
    .add("last")
    .build()
)
print(f"Built: {result}")
print()


print("=== Type Aliases ===")

# Simple type alias
Vector = list[float]
Matrix = list[list[float]]

# Complex type alias
JSONValue = Union[str, int, float, bool, None, list['JSONValue'], dict[str, 'JSONValue']]
Handler = Callable[[str, int], bool]
ResponseType = tuple[int, str, dict[str, Any]]


def process_vector(v: Vector) -> float:
    """Process a vector (list of floats)."""
    return sum(v)


vec: Vector = [1.0, 2.0, 3.0]
print(f"Vector sum: {process_vector(vec)}")
print()


print("=== Covariance and Contravariance ===")

# Covariant: TypeVar with covariant=True
T_co = TypeVar('T_co', covariant=True)

# Contravariant: TypeVar with contravariant=True
T_contra = TypeVar('T_contra', contravariant=True)


class Producer(Generic[T_co]):
    """Covariant producer - can only return T."""
    
    def __init__(self, value: T_co) -> None:
        self._value = value
    
    def get(self) -> T_co:
        return self._value


class Consumer(Generic[T_contra]):
    """Contravariant consumer - can only accept T."""
    
    def consume(self, value: T_contra) -> None:
        print(f"Consumed: {value}")


# Producer[Dog] can be used where Producer[Animal] is expected (covariant)
# Consumer[Animal] can be used where Consumer[Dog] is expected (contravariant)
print("Covariance: Producer[Subtype] -> Producer[Supertype]")
print("Contravariance: Consumer[Supertype] -> Consumer[Subtype]")
print()


print("=== Key Takeaways ===")
print("1. TypeVar for generic type parameters")
print("2. Generic for generic classes")
print("3. Protocol for structural typing (duck typing)")
print("4. Callable for function types")
print("5. Literal for specific value types")
print("6. TypedDict and NamedTuple for structured data")
print("7. @overload for multiple function signatures")
print("8. TypeGuard for type narrowing")
print("9. ParamSpec for preserving function signatures in decorators")

