# This script demonstrates function decorators
# Decorators are functions that modify the behavior of other functions

# Basic decorator example
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper


@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")


say_hello("Alice")
print()


# Practical example: timing decorator
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper


@timer
def slow_function():
    time.sleep(0.5)
    return "Done!"


print(slow_function())
print()


# Decorator with arguments
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3)
def greet(name):
    print(f"Greetings, {name}!")


greet("Bob")
print()


# Using functools.wraps to preserve function metadata
from functools import wraps


def smart_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper


@smart_decorator
def documented_function():
    """This is the original docstring."""
    pass


print(f"Function name: {documented_function.__name__}")
print(f"Function docstring: {documented_function.__doc__}")

