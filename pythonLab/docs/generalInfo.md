# **what is pydantic**

Its a library that validates an object for the correct types  
Pydantic lets you trust your data before your code touches it.

Ex:

```
from pydantic import BaseModel

userObj = {
    name: "Guru",
    age: 30
}
class User(BaseModel)
    age: int
    nam: str

user = User(**userObj)
```

So if the name is not a string , it will throw an error
It also does type conversion

Ex:

```
user = {age:"1"}
age = user.age + 1  // crash


```

```
USING PYDANTIC:
from pydantic import BaseModel
class User(BaseModel):
age: int

    user = User({age: "1"})
    print(User.age + 1)  // 2 Works

```

# **what is a decorator**

```
from pydantic import field_validator

class Address(BaseModel):
    pincode: int

    @field_validator("pincode")
    def check_pincode(cls, v):
        if len(str(v)) != 6:
            raise ValueError("pincode must be 6 digits")
        return v
```

@field_validator("pincode") - This is a decorator.  
@ is Python’s syntax for a decorator.  
A decorator means:

"Before or after this function runs, modify its behavior."  
Attach this function to the pincode validation pipeline.

# **what is ** in python\*\*

The symbol \* is used for unpacking or spreading lists or tuple  
 the symbol \*\* is used for unpacking or spreading dict[dictionary]

# **Difference in importing files**

import gradio as gr -> This imports the entire module/package and gives it an alias  
 from pypdf import PdfReader -> This imports only one class from the package.

# **Correct naming rules for Python files (modules)**

Python file names must:

- start with letter or underscore
- contain only letters, numbers, underscores
- cannot contain - or spaces

# ** Optimize code - caching methods without running it on every import **

    ```
        def one():
            ...

        def two():
            ...

        summary = f("using methods {one()} and {two()}")
    ```

    Instead of doing the above, we can cache the methods
    ```
        one = one()
        two = two()
        summary = f("using methods {one} and {two}")
    ```

    This ensures:

    ✅ runs only once
    ✅ result reused
    ✅ safe import behavior
    ✅ predictable performance

# ** What does load_dotenv do ? **

    Reads your .env file
    ✅ Loads variables into the environment
    ✅ Makes them available via os.getenv()

# **HTTPX VS requests**

    requests -> fetch() in JS
    HTTPX -> Promise.all() in JS
    Both are http clients .

    Both:
    Make HTTP calls
    Talk to APIs
    Send/receive JSON
    Handle headers, auth, timeouts

    # Difference = execution model
    requests (blocking, synchronous)
    ```
    response = requests.get(url)
    # Python waits here until done
    ```

    __Strengths__

    ✅ Dead simple
    ✅ Extremely stable
    ✅ Perfect for long-running tasks
    ✅ Ideal inside Celery workers
    ✅ Easier debugging

    __Weaknesses__
    ❌ Blocks the thread
    ❌ Slower when doing many calls in parallel

    httpx (async-first, modern)
    ```
    async with httpx.AsyncClient() as client:
    response = await client.get(url)
    ```

    Python:
    Starts request
    Does other work
    Comes back when response is ready

    __Strengths__
    ✅ High concurrency
    ✅ Fast for many tool calls
    ✅ Async + sync support
    ✅ HTTP/2, connection pooling
    __Weaknesses__
    ❌ More complex
    ❌ Requires async discipline
    ❌ Harder stack traces

    1) requests can be used for celery tasks that can be bocked as it runs parallely.Needs more time and this is where the agents think. Blocking is fine
    Reliability > speed
    2) HTTPX can be used multiple api calls
    Streaming responses
    Concurrent planners

# Python Decorators – Complete Guide

## 📌 What is a Decorator?

A **decorator** is:

> A function that modifies another function’s behavior without changing its code. Basically, an Higher order component in JS

Decorators allow you to wrap additional functionality around an existing function in a clean and reusable way.

---

## 🎁 Simple Analogy

Think of a function as a gift box.

A decorator is gift wrapping:

- The box (function) stays the same.
- You add something outside it.

---

## 🔹 Basic Function (No Decorator)

```python
def greet():
    print("Hello")
```

Now suppose you want to log whenever it runs:

```python
def greet():
    print("Function started")
    print("Hello")
    print("Function ended")
```

If you need this behavior for 20 functions, repeating this is bad practice.

Decorators solve this problem.

---

## 🔹 Basic Decorator Example

```python
def my_decorator(func):
    def wrapper():
        print("Function started")
        func()
        print("Function ended")
    return wrapper
```

Apply it:

```python
@my_decorator
def greet():
    print("Hello")

greet()
```

### Output:

```
Function started
Hello
Function ended
```

---

## 🔹 What `@decorator` Actually Means

This:

```python
@my_decorator
def greet():
```

Is the same as:

```python
greet = my_decorator(greet)
```

The decorator wraps the original function and returns a modified version.

---

## 🔹 Production-Ready Decorator Pattern

Always support arguments using `*args` and `**kwargs`.

```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}")
        result = func(*args, **kwargs)
        print("Done")
        return result
    return wrapper
```

Usage:

```python
@log_execution
def calculate(x, y):
    return x + y

calculate(5, 3)
```

---

## 🔹 Real-World Production Use Cases

Decorators are used for:

- Logging
- Authentication
- Caching
- Rate limiting
- Error handling
- Timing functions
- API route registration (FastAPI, Flask)

---

## 🔹 Example: Timing Decorator (Useful for AI Inference)

```python
import time

def time_execution(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start:.2f}s")
        return result
    return wrapper
```

Apply it to an AI call:

```python
@time_execution
def run_agent(prompt):
    return Runner.run_sync(agent, prompt)
```

---

## 🔹 Built-in Decorators in Python

You already use these:

- `@staticmethod`
- `@classmethod`
- `@property`

Example:

```python
class Person:
    @property
    def name(self):
        return "Guru"
```

---

## 🔹 Why Decorators Matter in AI Applications

In production AI systems, decorators help you:

- Log agent calls
- Track inference time
- Add retry logic for API failures
- Add authentication to endpoints
- Monitor usage

Instead of modifying core logic, you wrap behavior cleanly.

---

## 🔹 Mental Model

Without decorator:

```
Function → Runs
```

With decorator:

```
Decorator → Function → Return
```

The decorator wraps and enhances the function.

---

## 🔹 Technical Definition

A decorator is:

> A higher-order function that takes a function and returns a new function.

---

## 🔹 Key Takeaways

| Concept        | Meaning                                       |
| -------------- | --------------------------------------------- |
| Decorator      | Function that wraps another function          |
| Syntax         | `@decorator_name`                             |
| Purpose        | Modify behavior without editing original code |
| Production Use | Logging, auth, caching, monitoring            |

---

## 🚀 Summary

Decorators allow you to:

- Keep your core logic clean
- Add reusable enhancements
- Write production-ready, scalable Python code

They are fundamental in modern Python frameworks and AI backend systems.
