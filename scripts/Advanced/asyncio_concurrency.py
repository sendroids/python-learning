# This script demonstrates asynchronous programming with asyncio
# Async programming allows concurrent execution without threads

import asyncio
from typing import List
import time

# Basic async function (coroutine)
async def say_hello(name: str, delay: float) -> str:
    """Async function that greets after a delay."""
    await asyncio.sleep(delay)  # Non-blocking sleep
    message = f"Hello, {name}!"
    print(message)
    return message


# Running a single coroutine
print("=== Basic Async Function ===")
result = asyncio.run(say_hello("Alice", 0.1))
print(f"Returned: {result}")
print()


# Running multiple coroutines concurrently with gather
async def greet_many():
    """Run multiple greetings concurrently."""
    # These run concurrently, not sequentially!
    results = await asyncio.gather(
        say_hello("Alice", 0.3),
        say_hello("Bob", 0.2),
        say_hello("Charlie", 0.1),
    )
    return results


print("=== Concurrent Execution with gather() ===")
start = time.time()
results = asyncio.run(greet_many())
print(f"All results: {results}")
print(f"Total time: {time.time() - start:.2f}s (not 0.6s because concurrent!)")
print()


# Creating and managing tasks
async def fetch_data(source: str, delay: float) -> dict:
    """Simulate fetching data from different sources."""
    print(f"Starting fetch from {source}...")
    await asyncio.sleep(delay)
    return {"source": source, "data": f"Data from {source}"}


async def process_with_tasks():
    """Create and manage individual tasks."""
    # Create tasks - they start running immediately
    task1 = asyncio.create_task(fetch_data("API", 0.3))
    task2 = asyncio.create_task(fetch_data("Database", 0.2))
    task3 = asyncio.create_task(fetch_data("Cache", 0.1))
    
    # Wait for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    return results


print("=== Working with Tasks ===")
results = asyncio.run(process_with_tasks())
for r in results:
    print(f"  {r}")
print()


# Handling timeouts
async def slow_operation():
    """A slow operation that might timeout."""
    await asyncio.sleep(5)
    return "Completed"


async def with_timeout():
    """Demonstrate timeout handling."""
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.5)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")


print("=== Timeout Handling ===")
asyncio.run(with_timeout())
print()


# Task cancellation
async def cancellable_task():
    """A task that can be cancelled."""
    try:
        print("Task started...")
        await asyncio.sleep(10)
        print("Task completed!")
    except asyncio.CancelledError:
        print("Task was cancelled!")
        raise  # Re-raise to properly handle cancellation


async def cancel_demo():
    """Demonstrate task cancellation."""
    task = asyncio.create_task(cancellable_task())
    await asyncio.sleep(0.1)  # Let the task start
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Caught cancellation in main")


print("=== Task Cancellation ===")
asyncio.run(cancel_demo())
print()


# Async context managers
class AsyncResource:
    """Async context manager for resource management."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        print(f"Acquiring {self.name}...")
        await asyncio.sleep(0.1)
        print(f"Acquired {self.name}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing {self.name}...")
        await asyncio.sleep(0.1)
        print(f"Released {self.name}")
        return False


async def use_async_context():
    """Use async context manager."""
    async with AsyncResource("DatabaseConnection") as resource:
        print(f"Using {resource.name}")


print("=== Async Context Managers ===")
asyncio.run(use_async_context())
print()


# Async iterators and generators
class AsyncCounter:
    """Async iterator that counts with delays."""
    
    def __init__(self, stop: int):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        self.current += 1
        await asyncio.sleep(0.1)
        return self.current


async def async_generator(n: int):
    """Async generator function."""
    for i in range(n):
        await asyncio.sleep(0.05)
        yield i * 2


async def iterate_async():
    """Demonstrate async iteration."""
    print("Async iterator:")
    async for num in AsyncCounter(3):
        print(f"  Count: {num}")
    
    print("Async generator:")
    async for value in async_generator(4):
        print(f"  Value: {value}")


print("=== Async Iterators and Generators ===")
asyncio.run(iterate_async())
print()


# Semaphores for limiting concurrency
async def limited_operation(semaphore: asyncio.Semaphore, task_id: int):
    """Operation that respects semaphore limits."""
    async with semaphore:
        print(f"Task {task_id} acquired semaphore")
        await asyncio.sleep(0.2)
        print(f"Task {task_id} releasing semaphore")
        return task_id


async def limited_concurrency():
    """Run tasks with limited concurrency using semaphore."""
    semaphore = asyncio.Semaphore(2)  # Only 2 concurrent operations
    tasks = [limited_operation(semaphore, i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    return results


print("=== Semaphores for Rate Limiting ===")
print("Running 5 tasks with max 2 concurrent:")
asyncio.run(limited_concurrency())
print()


# Event synchronization
async def waiter(event: asyncio.Event, name: str):
    """Wait for an event to be set."""
    print(f"{name} waiting for event...")
    await event.wait()
    print(f"{name} received event!")


async def setter(event: asyncio.Event):
    """Set an event after a delay."""
    await asyncio.sleep(0.3)
    print("Setting event...")
    event.set()


async def event_demo():
    """Demonstrate event synchronization."""
    event = asyncio.Event()
    await asyncio.gather(
        waiter(event, "Waiter1"),
        waiter(event, "Waiter2"),
        setter(event),
    )


print("=== Event Synchronization ===")
asyncio.run(event_demo())
print()


# Producer-consumer pattern with Queue
async def producer(queue: asyncio.Queue, items: List[str]):
    """Produce items to the queue."""
    for item in items:
        await asyncio.sleep(0.1)
        await queue.put(item)
        print(f"Produced: {item}")
    await queue.put(None)  # Signal end


async def consumer(queue: asyncio.Queue):
    """Consume items from the queue."""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        queue.task_done()


async def producer_consumer():
    """Demonstrate producer-consumer pattern."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=3)
    items = ["apple", "banana", "cherry", "date"]
    
    await asyncio.gather(
        producer(queue, items),
        consumer(queue),
    )


print("=== Producer-Consumer Pattern ===")
asyncio.run(producer_consumer())
print()


# Exception handling in concurrent tasks
async def might_fail(task_id: int, should_fail: bool):
    """Task that might raise an exception."""
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError(f"Task {task_id} failed!")
    return f"Task {task_id} succeeded"


async def handle_exceptions():
    """Handle exceptions from concurrent tasks."""
    tasks = [
        might_fail(1, False),
        might_fail(2, True),
        might_fail(3, False),
    ]
    
    # return_exceptions=True returns exceptions as results instead of raising
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1}: Error - {result}")
        else:
            print(f"Task {i+1}: {result}")


print("=== Exception Handling in Concurrent Tasks ===")
asyncio.run(handle_exceptions())
print()


# Real-world example: Async HTTP-like requests (simulated)
async def http_get(url: str) -> dict:
    """Simulate an async HTTP GET request."""
    delay = len(url) * 0.01  # Variable delay based on URL length
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "data": f"Response from {url}"}


async def fetch_all_urls():
    """Fetch multiple URLs concurrently."""
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/albums",
    ]
    
    start = time.time()
    responses = await asyncio.gather(*[http_get(url) for url in urls])
    elapsed = time.time() - start
    
    print(f"Fetched {len(urls)} URLs in {elapsed:.3f}s")
    for response in responses:
        print(f"  {response['url']} -> {response['status']}")


print("=== Real-World: Concurrent HTTP Requests (Simulated) ===")
asyncio.run(fetch_all_urls())
print()

print("=== Key Takeaways ===")
print("1. Use 'async def' to define coroutines")
print("2. Use 'await' to wait for async operations")
print("3. Use asyncio.gather() for concurrent execution")
print("4. Use asyncio.create_task() for background tasks")
print("5. Async is great for I/O-bound operations (network, files)")
print("6. Not suitable for CPU-bound operations (use multiprocessing instead)")

