# Context Manager and `yield` in Python — Complete Guide

## Table of Contents

- What is a Context Manager
- Why Context Managers are Needed
- How `with` Works Internally
- Using `yield` to Create Context Managers
- Async Context Managers
- Real-World Examples
- Interview Questions
- Summary

---

# What is a Context Manager

A **context manager** is a Python object that automatically manages resources.

It ensures:

- Setup is done properly
- Cleanup is done automatically
- Even if errors occur

It is used with the `with` statement.

Example:

```python
with open("file.txt", "r") as f:
    content = f.read()
```

The file is automatically closed.

---

# Why Context Managers are Needed

Without context manager:

```python
f = open("file.txt", "r")
content = f.read()
f.close()
```

Problem:

If error occurs before `close()`, file stays open.

This causes:

- Memory leaks
- Resource leaks
- Performance issues

Context manager solves this.

---

# How `with` Works Internally

Context manager uses two special methods:

```python
__enter__()
__exit__()
```

Example:

```python
class MyContext:

    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc, traceback):
        print("Exiting")


with MyContext():
    print("Inside block")
```

Output:

```
Entering
Inside block
Exiting
```

Flow:

```
__enter__ → block runs → __exit__
```

---

# What is `yield`

`yield` pauses a function and resumes later.

Example:

```python
def test():
    print("Start")
    yield
    print("End")
```

---

# Creating Context Manager using `yield`

Instead of writing class, Python provides:

`contextlib.contextmanager`

Example:

```python
from contextlib import contextmanager

@contextmanager
def my_context():

    print("Before")

    yield

    print("After")


with my_context():
    print("Inside")
```

Output:

```
Before
Inside
After
```

Explanation:

- Code before `yield` → acts like `__enter__`
- Code after `yield` → acts like `__exit__`

---

# Async Context Manager

Used when working with async code.

Uses:

```
async with
```

Example:

```python
import httpx

async with httpx.AsyncClient() as client:

    response = await client.get("https://google.com")
```

---

# Creating Async Context Manager using `yield`

Use:

```python
asynccontextmanager
```

Example:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_client():

    print("Opening")

    yield "client"

    print("Closing")


async with get_client() as client:
    print(client)
```

Output:

```
Opening
client
Closing
```

---

# Real-World Examples

## File handling

```python
with open("file.txt") as f:
    data = f.read()
```

---

## HTTP Client

```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

---

## Database connection

```python
with sqlite3.connect("db.sqlite") as conn:
    pass
```

---

# Why `yield` is used instead of `return`

`return` ends function permanently.

`yield` pauses function and resumes later.

This allows:

- Setup before yield
- Cleanup after yield

---

# Internal Flow using yield

This:

```python
@contextmanager
def example():

    setup()

    yield resource

    cleanup()
```

Equivalent to:

```python
class Example:

    def __enter__(self):
        setup()
        return resource

    def __exit__(self):
        cleanup()
```

---

# Interview Questions

## Question:

What is a context manager?

Answer:

A context manager is an object that manages resources using `__enter__` and `__exit__` methods and is used with the `with` statement.

---

## Question:

Why use yield in context manager?

Answer:

Yield allows splitting setup and cleanup logic without writing a class.

---

## Question:

Difference between return and yield

Return:

- Ends function

Yield:

- Pauses and resumes function

---

# When You Will Use This in Real Projects

Very common in:

- OpenAI API
- FastAPI
- Database connections
- HTTP clients
- File handling
- AI agents

Example:

```python
async with AsyncOpenAI() as client:
```

---

# Summary

Context manager ensures:

- Proper resource management
- Automatic cleanup
- Cleaner code

`yield` helps create context managers easily.

Async version supports async code.

---

# Key Takeaway

Context manager lifecycle:

```
Setup → yield → block executes → cleanup
```

---

# End
