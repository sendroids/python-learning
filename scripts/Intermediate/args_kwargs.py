# This script demonstrates *args and **kwargs in Python
# These allow functions to accept variable numbers of arguments

# *args - accepts any number of positional arguments
def sum_all(*args):
    """Sum any number of arguments."""
    print(f"Received args: {args}")  # args is a tuple
    return sum(args)


print(f"sum_all(1, 2): {sum_all(1, 2)}")
print(f"sum_all(1, 2, 3, 4, 5): {sum_all(1, 2, 3, 4, 5)}")
print()


# **kwargs - accepts any number of keyword arguments
def print_info(**kwargs):
    """Print key-value pairs."""
    print(f"Received kwargs: {kwargs}")  # kwargs is a dict
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


print("print_info(name='Alice', age=30, city='NYC'):")
print_info(name="Alice", age=30, city="NYC")
print()


# Combining regular args, *args, and **kwargs
def full_function(required, *args, default="default_value", **kwargs):
    """Function with all argument types."""
    print(f"Required: {required}")
    print(f"*args: {args}")
    print(f"default: {default}")
    print(f"**kwargs: {kwargs}")


print("full_function('must_have', 1, 2, 3, default='custom', extra='bonus'):")
full_function("must_have", 1, 2, 3, default="custom", extra="bonus")
print()


# Unpacking with * and **
def greet(greeting, name, punctuation):
    return f"{greeting}, {name}{punctuation}"


# Unpack list/tuple with *
args_list = ["Hello", "World", "!"]
print(f"Unpacking list: {greet(*args_list)}")

# Unpack dict with **
kwargs_dict = {"greeting": "Hi", "name": "Python", "punctuation": "?"}
print(f"Unpacking dict: {greet(**kwargs_dict)}")
print()


# Practical example: wrapper function
def logged_function(func, *args, **kwargs):
    """Call function with logging."""
    print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
    result = func(*args, **kwargs)
    print(f"Result: {result}")
    return result


def multiply(a, b, verbose=False):
    result = a * b
    if verbose:
        print(f"  {a} * {b} = {result}")
    return result


print("Using wrapper function:")
logged_function(multiply, 3, 4, verbose=True)
print()


# Keyword-only arguments (after *)
def configure(*, host, port, debug=False):
    """Function with keyword-only arguments."""
    print(f"Host: {host}, Port: {port}, Debug: {debug}")


# Must use keyword arguments
configure(host="localhost", port=8080)
configure(host="0.0.0.0", port=80, debug=True)
print()


# Positional-only arguments (before /)
def divide(x, y, /):
    """Function with positional-only arguments."""
    return x / y


print(f"divide(10, 2): {divide(10, 2)}")
# divide(x=10, y=2) would raise TypeError
print()


# Combining positional-only, regular, and keyword-only
def complex_function(pos_only, /, standard, *, kw_only):
    """
    pos_only: positional-only (before /)
    standard: can be positional or keyword
    kw_only: keyword-only (after *)
    """
    return f"pos_only={pos_only}, standard={standard}, kw_only={kw_only}"


print(complex_function(1, 2, kw_only=3))
print(complex_function(1, standard=2, kw_only=3))
print()


# Real-world example: flexible data processor
def process_data(data, *transformations, validate=True, **options):
    """
    Process data with flexible transformations and options.
    
    Args:
        data: The data to process
        *transformations: Functions to apply in sequence
        validate: Whether to validate input
        **options: Additional processing options
    """
    print(f"Processing data: {data}")
    print(f"Transformations: {len(transformations)}")
    print(f"Validate: {validate}")
    print(f"Options: {options}")
    
    result = data
    for transform in transformations:
        result = transform(result)
    return result


result = process_data(
    "hello",
    str.upper,
    str.strip,
    validate=True,
    encoding="utf-8",
    max_length=100
)
print(f"Final result: {result}")

