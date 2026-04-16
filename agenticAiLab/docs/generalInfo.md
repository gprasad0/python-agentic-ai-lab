# **Difference bw system and user prompts**

System Prompt — "WHO the AI is and HOW it should behave"  
Purpose:  
Sets the rules, personality, constraints, and style for the assistant.
This is internal instruction to the AI.  
Think:  
System prompt = Operating System  
Ex :

```
    {
  "role": "system",
  "content": "You are a startup advisor. Always analyze ideas by market size, feasibility, profit potential, and scalability. Give structured output."
  }
```

User Prompt — "WHAT the user wants right now"  
Purpose:
It contains:
The actual question
The data
The user’s request
This is your runtime input.

```
{
  "role": "user",
  "content": f"tell me the best idea... {businessResults}"
}

```

# **load_dotenv(override=True)**

The command load_dotenv(override=True) is used in Python with the python-dotenv library to load environment variables from a .env file and, importantly, force them to replace any existing environment variables in your system's current session.  
 By default, when you use load_dotenv() without the override parameter (which defaults to False), existing system environment variables take precedence over those defined in your .env file

# **Whats the use of paranthesis in a list + expression format for prompts**

```
   messages = (
        [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        + history
        + [
            {"role": "user", "content": message},
        ]
    )
```

The parentheses don’t create a tuple here.
They’re only used to make the expression span multiple lines cleanly. SO basically , it allows to write in multiple lines but the list addition will be the same
Ex : [1,3] + [4,5] + [6,9] => [1,3,4,5,6,9] -> so it allows multiple lines . One long expression

# \*\* \*\*

### `*chat_history` (List Unpacking)

```python
*chat_history
```

This uses Python’s **list unpacking** feature.

If `chat_history` is:

```python
[
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello"}
]
```

Then `*chat_history` expands to:

```python
{"role": "user", "content": "Hi"},
{"role": "assistant", "content": "Hello"}
```

This inserts all previous messages directly into the `messages` list while
preserving their original order.

---

### ** what is an agent**

    An agent is an LLM that uses tools in a loop to acheive a specific goal

### ** what is inference**

    Inference = When a trained model is used to make a prediction.
    When you run:
    result = Runner.run_sync(agent, "Tell my fortune")
    That call is inference.
    Meaning:
    The model is already trained
    You send input
    It predicts next tokens
    It returns output
    That prediction step = inference.

# Python `append()` vs `extend()`

In Python, both **`append()`** and **`extend()`** are list methods used to add elements to a list.
However, they behave differently when adding multiple elements.

Understanding the difference is important when working with lists and avoiding unintended nested lists.

---

# append()

## Definition

`append()` adds **a single element** to the end of a list.

If the element itself is a list, the **entire list is added as a single item**, creating a nested list.

## Syntax

```python
list.append(element)
```

## Example

```python
numbers = [1, 2, 3]

numbers.append(4)

print(numbers)
```

Output:

```
[1, 2, 3, 4]
```

---

## Appending a List

```python
numbers = [1, 2, 3]

numbers.append([4, 5])

print(numbers)
```

Output:

```
[1, 2, 3, [4, 5]]
```

Notice that `[4, 5]` becomes a **nested list inside the main list**.

---

# extend()

## Definition

`extend()` adds **each element from another iterable** to the list.

Instead of adding the iterable as one item, it **iterates through it and appends each element individually**.

## Syntax

```python
list.extend(iterable)
```

## Example

```python
numbers = [1, 2, 3]

numbers.extend([4, 5])

print(numbers)
```

Output:

```
[1, 2, 3, 4, 5]
```

The elements `4` and `5` are **added individually**.

---

# Visual Difference

### append()

```
[1, 2, 3] + [4, 5]
        ↓
[1, 2, 3, [4, 5]]
```

### extend()

```
[1, 2, 3] + [4, 5]
        ↓
[1, 2, 3, 4, 5]
```

---

# Side-by-Side Example

```python
a = [1, 2, 3]

a.append([4, 5])
print(a)
```

Output

```
[1, 2, 3, [4, 5]]
```

---

```python
a = [1, 2, 3]

a.extend([4, 5])
print(a)
```

Output

```
[1, 2, 3, 4, 5]
```

---

# Comparison Table

| Feature             | append()             | extend()          |
| ------------------- | -------------------- | ----------------- |
| Adds                | One element          | Multiple elements |
| Accepts             | Any object           | Iterable          |
| Nested list created | Yes (if list passed) | No                |
| Typical use case    | Add a single item    | Merge lists       |

---

# Rule of Thumb

Use:

```
append() → when adding one item
extend() → when merging lists
```

---

# Example Use Case

### Using append

```python
tools = []

tools.append("weather_tool")
tools.append("email_tool")
```

Result

```
["weather_tool", "email_tool"]
```

---

### Using extend

```python
tools = ["weather_tool"]

tools.extend(["email_tool", "notification_tool"])
```

Result

```
["weather_tool", "email_tool", "notification_tool"]
```

---

# Alternative (Pythonic Way)

Sometimes you can simply combine lists:

```python
tools = ["weather_tool"] + ["email_tool", "notification_tool"]
```

Result

```
["weather_tool", "email_tool", "notification_tool"]
```

---

# Summary

- `append()` adds **one element to the list**
- `extend()` adds **elements from another iterable**

Choosing the correct method prevents **unexpected nested lists and improves code clarity**.

# 📘 TypedDict vs Annotated vs BaseModel (Pydantic)

This guide explains the difference between three commonly used constructs in modern Python systems:

- `TypedDict`
- `typing.Annotated`
- `pydantic.BaseModel`

These are often used together in frameworks like **FastAPI**, **LangGraph**, and **AI agent systems**, but they serve **completely different purposes**.

---

## 🧠 TL;DR

| Concept     | Purpose                                                    |
| ----------- | ---------------------------------------------------------- |
| `TypedDict` | Defines the shape of a dictionary (no runtime enforcement) |
| `Annotated` | Adds metadata to a type                                    |
| `BaseModel` | Defines and validates structured data                      |

> ❗ These are **not interchangeable** — they operate at different layers.

---

## 🔹 1. TypedDict

```python
from typing_extensions import TypedDict

class State(TypedDict):
    name: str
    age: int
```

### ✅ What it does

- Defines the **expected keys and types** of a dictionary
- Helps with:
  - IDE autocomplete
  - Static type checking (mypy)

### ❌ What it does NOT do

- No runtime validation
- No error if types are wrong

```python
state: State = {"name": 123, "age": "wrong"}  # ✅ No runtime error
```

### 🧠 Mental Model

> “This dictionary should look like this”

---

## 🔹 2. Annotated

```python
from typing import Annotated
from pydantic import Field

age: Annotated[int, Field(gt=0, lt=120)]
```

### ✅ What it does

- Attaches **metadata** to a type
- Used by frameworks for:
  - Validation rules
  - Behavior (e.g., reducers in LangGraph)

### ❌ What it does NOT do

- Does not create objects
- Does not validate by itself

### 🧠 Mental Model

> “This is still an `int`, but with extra instructions”

---

## 🔹 3. BaseModel (Pydantic)

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

### ✅ What it does

- Defines a **structured data model**
- Performs **runtime validation**
- Parses input (e.g., JSON → Python object)

```python
User(name=123, age="abc")  # ❌ Raises validation error
```

### 🧠 Mental Model

> “This is a strict contract for data”

---

## ⚔️ Side-by-Side Comparison

| Feature            | TypedDict    | Annotated            | BaseModel    |
| ------------------ | ------------ | -------------------- | ------------ |
| Purpose            | Dict shape   | Metadata             | Data schema  |
| Runtime validation | ❌           | ❌                   | ✅           |
| Creates object     | ❌           | ❌                   | ✅           |
| Runtime behavior   | None         | None                 | Active       |
| Use case           | State/config | Constraints/behavior | API/LLM data |

---

## 🔥 How They Work Together

### Example (LangGraph / AI system)

#### 🧠 State (TypedDict + Annotated)

```python
from typing import Annotated, List, Any
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
```

- `TypedDict` → defines structure
- `Annotated` → defines behavior (merge strategy)

---

#### 📜 Output (BaseModel)

```python
from pydantic import BaseModel

class EvaluatorOutput(BaseModel):
    feedback: str
    success_criteria_met: bool
```

- Validates LLM output
- Ensures structured data

---

## 🧠 Design Principles

### ✅ Use `TypedDict` when:

- You need lightweight state
- You don’t need runtime validation
- Example: Graph state, config

---

### ✅ Use `Annotated` when:

- You want to attach metadata or behavior
- Example:
  - Validation constraints (`Field`, `Query`)
  - LangGraph reducers (`add_messages`)

---

### ✅ Use `BaseModel` when:

- You need validated, structured data
- Example:
  - API request/response
  - LLM outputs
  - Tool interfaces

---

## ❌ Common Mistakes

- Expecting `TypedDict` to validate data ❌
- Using `Annotated` as a replacement for validation ❌
- Using `BaseModel` for lightweight state (overkill) ❌

---

## 📌 Summary

| Layer                   | Tool        |
| ----------------------- | ----------- |
| Structure (lightweight) | `TypedDict` |
| Metadata / Behavior     | `Annotated` |
| Validation / Contracts  | `BaseModel` |

---

## 💡 Final Takeaway

> Build robust systems by separating concerns:

- **Shape** → `TypedDict`
- **Metadata** → `Annotated`
- **Validation** → `BaseModel`

This leads to:

- Cleaner architecture
- Better performance
- Safer AI systems

---
