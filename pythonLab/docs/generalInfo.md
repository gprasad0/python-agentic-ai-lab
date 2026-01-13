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
