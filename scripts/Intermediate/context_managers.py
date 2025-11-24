# This script demonstrates custom context managers
# Context managers handle setup and cleanup using the 'with' statement

# Method 1: Using a class with __enter__ and __exit__
class FileManager:
    """Custom context manager for file handling."""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        # Return False to propagate exceptions, True to suppress them
        return False


# Using the custom file manager
with FileManager("test_file.txt", "w") as f:
    f.write("Hello from custom context manager!")

print()


# Method 2: Using contextlib.contextmanager decorator
from contextlib import contextmanager


@contextmanager
def timer_context(label):
    """Context manager that times code execution."""
    import time
    start = time.time()
    print(f"Starting: {label}")
    try:
        yield  # Code in 'with' block runs here
    finally:
        elapsed = time.time() - start
        print(f"Finished: {label} (took {elapsed:.4f} seconds)")


with timer_context("Some operation"):
    import time
    time.sleep(0.1)
    print("Doing some work...")

print()


# Practical example: Database connection manager
@contextmanager
def database_connection(db_name):
    """Simulated database connection context manager."""
    print(f"Connecting to database: {db_name}")
    connection = {"db": db_name, "status": "connected"}
    try:
        yield connection
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Rolling back transaction...")
        raise
    finally:
        print(f"Closing connection to {db_name}")


with database_connection("users_db") as conn:
    print(f"Working with {conn['db']}")
    print("Inserting data...")
    print("Querying data...")

print()


# Context manager for changing directories temporarily
import os


@contextmanager
def change_directory(path):
    """Temporarily change working directory."""
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        print(f"Changed to: {os.getcwd()}")
        yield
    finally:
        os.chdir(original_dir)
        print(f"Restored to: {os.getcwd()}")


# Example (commented out to avoid path issues):
# with change_directory("/tmp"):
#     print("Doing work in /tmp")
print()


# Context manager for suppressing exceptions
from contextlib import suppress

print("Using suppress context manager:")
with suppress(FileNotFoundError):
    with open("nonexistent_file.txt", "r") as f:
        content = f.read()
print("Continued after suppressed exception")
print()


# Multiple context managers
print("Using multiple context managers:")
with FileManager("file1.txt", "w") as f1, FileManager("file2.txt", "w") as f2:
    f1.write("Content for file 1")
    f2.write("Content for file 2")
print()


# Context manager for acquiring and releasing resources
class ResourcePool:
    """Simulated resource pool with context manager."""
    
    def __init__(self, name, max_resources=3):
        self.name = name
        self.available = max_resources
    
    @contextmanager
    def acquire(self):
        if self.available <= 0:
            raise RuntimeError("No resources available")
        self.available -= 1
        print(f"Acquired resource from {self.name}. Available: {self.available}")
        try:
            yield f"resource_{self.available + 1}"
        finally:
            self.available += 1
            print(f"Released resource to {self.name}. Available: {self.available}")


pool = ResourcePool("ConnectionPool")
with pool.acquire() as resource:
    print(f"Using {resource}")

# Cleanup test files
import os
for f in ["test_file.txt", "file1.txt", "file2.txt"]:
    if os.path.exists(f):
        os.remove(f)

