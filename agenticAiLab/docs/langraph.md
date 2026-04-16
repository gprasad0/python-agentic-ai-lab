# 📩 `add_messages` in LangGraph

## 🧠 What is `add_messages`?

```python
from langgraph.graph.message import add_messages
```

`add_messages` is a **reducer function** used in LangGraph to **merge message lists across state updates**.

It is most commonly used with `Annotated` inside a `TypedDict` state.

---

## 🔹 Why do we need it?

In LangGraph, multiple nodes update the shared `State`.

Without a reducer:

- New values would **overwrite** old ones ❌

With `add_messages`:

- Messages are **appended / merged correctly** ✅

---

## 🔹 Basic Usage

```python
from typing import Annotated, List, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
```

---

## 🔍 What this means

```python
messages: Annotated[List[Any], add_messages]
```

- `List[Any]` → your message history
- `add_messages` → how updates are applied

👉 Instead of replacing messages, LangGraph will **append new ones**

---

## 🔄 Without vs With `add_messages`

### ❌ Without reducer

```python
state["messages"] = ["new message"]
```

➡️ Old messages are LOST

---

### ✅ With `add_messages`

```python
state["messages"] + ["new message"]
```

➡️ Messages are PRESERVED and appended

---

## 🔧 How it works internally

When a node returns:

```python
return {"messages": [new_message]}
```

LangGraph:

1. Looks at `Annotated`
2. Finds `add_messages`
3. Applies merge logic:

   ```
   existing_messages + new_messages
   ```

---

## 🧠 Mental Model

> `add_messages` = “append to conversation history instead of replacing it”

---

## 🚀 Real Example (Agent Flow)

### Initial State

```python
state = {
    "messages": ["User: Hello"]
}
```

---

### Node Output

```python
return {
    "messages": ["Assistant: Hi!"]
}
```

---

### Final State (after reducer)

```python
state = {
    "messages": [
        "User: Hello",
        "Assistant: Hi!"
    ]
}
```

---

## 💡 Why it's important

Without `add_messages`:

- Your agent will **forget previous context**

With `add_messages`:

- You maintain **conversation memory**
- Essential for:
  - Chatbots
  - Multi-step reasoning
  - Agent loops

---

## ⚠️ Common Mistakes

### ❌ Forgetting to use `Annotated`

```python
messages: List[Any]  # No reducer → overwrite bug
```

---

### ❌ Expecting automatic merging without reducer

LangGraph **does NOT merge by default**

---

## 🧩 Best Practices

- Always use `add_messages` for:
  - Chat history
  - LLM message tracking

- Keep messages structured (e.g., role/content format)

- Combine with:
  - `TypedDict` → state structure
  - `BaseModel` → LLM output validation

---

## 📌 Summary

| Concept        | Role                 |
| -------------- | -------------------- |
| `messages`     | Conversation history |
| `Annotated`    | Attach reducer       |
| `add_messages` | Merge strategy       |

---

## 🧠 Final Takeaway

> In LangGraph, state updates are not automatic —
> **reducers like `add_messages` define how data evolves.**

Without it, your agent loses memory.
With it, your agent becomes stateful and intelligent.

---

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
