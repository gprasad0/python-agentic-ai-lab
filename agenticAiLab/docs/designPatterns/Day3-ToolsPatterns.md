## Tool Input Schema in Agentic AI

### Why `type: "object"` and `properties` Exist

When building **agentic AI systems**, tools are not called using free-form text.  
Each tool defines a **strict input schema** using **JSON Schema**.

This schema acts as a **contract** between the LLM and your application code.

---

## Example Tool Schema

```json
{
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "description": "User email address"
    },
    "name": {
      "type": "string",
      "description": "User's full name"
    }
  },
  "required": ["email"]
}
```

---

## Why `type: "object"`?

This tells the LLM:

> When calling this tool, the arguments must be provided as **one JSON object**.

Without `type: "object"`, the model does not know how to structure inputs and may
produce unstructured or invalid text.

### Correct tool call output

```json
{
  "email": "user@example.com",
  "name": "Guru"
}
```

---

## What does `properties` do?

`properties` defines the **fields allowed inside the object** and their expected data types.

In this example:

- `email` must be a string
- `name` must be a string

Any field not listed in `properties` is considered invalid.

---

## Why JSON Schema Is Critical in Agentic AI

LLMs naturally generate free-form text and may hallucinate.

### Without a schema

```text
The user's email is guru@gmail.com and his name is Guru
```

### With a schema

```json
{
  "email": "guru@gmail.com",
  "name": "Guru"
}
```

JSON Schema forces the model to output **machine-readable, validated data**.

---

## Why This Matters

- **Reliable tool execution** – predictable inputs
- **Automatic validation** – invalid calls are rejected early
- **Deterministic agent behavior** – fewer runtime failures
- **Reduced hallucination** – strict structure guides the model

---

## Mental Model

Think of tool schemas as **types for LLMs**:

| Traditional Development | Agentic AI            |
| ----------------------- | --------------------- |
| Function parameters     | Tool arguments        |
| TypeScript types        | JSON Schema           |
| Runtime type checks     | Tool input validation |

This is effectively **TypeScript for LLM tool calls**, enforced at runtime.

---

## Required Fields

```json
"required": ["email"]
```

This enforces that the model **must include** the `email` field when calling the tool.
If missing, the call is treated as invalid.

---

## Summary

- `type: "object"` → tool expects a single JSON object
- `properties` → defines allowed fields and their data types
- This uses **JSON Schema**, not arbitrary JSON
- Schemas are essential for **production-grade agentic AI systems**
