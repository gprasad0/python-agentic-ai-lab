# Working with JSON Data in SQLite

## Overview

SQLite does not have a native Python dictionary or list type.

When storing complex objects such as:

- Research results
- Proposal sections
- Retrieved context
- Review feedback
- Parsed company data

the data must first be converted into a JSON string.

The standard approach is:

```text
Python Dict/List
        ↓
    json.dumps()
        ↓
    JSON String
        ↓
SQLite TEXT Column
```

When reading data back:

```text
SQLite TEXT Column
        ↓
    JSON String
        ↓
    json.loads()
        ↓
Python Dict/List
```

---

## Writing JSON Data

Example Python object:

```python
research_data = {
    "company": "Acme",
    "industry": "Fintech",
    "employees": 500
}
```

Convert to JSON before saving:

```python
import json

cursor.execute(
    """
    UPDATE proposals
    SET research_data = ?
    WHERE id = ?
    """,
    (
        json.dumps(research_data),
        proposal_id,
    ),
)

conn.commit()
```

Stored value in SQLite:

```json
{
  "company": "Acme",
  "industry": "Fintech",
  "employees": 500
}
```

Internally, SQLite stores this as plain text.

---

## Reading JSON Data

Retrieve the value from SQLite:

```python
cursor.execute(
    """
    SELECT research_data
    FROM proposals
    WHERE id = ?
    """,
    (proposal_id,)
)

row = cursor.fetchone()
```

Convert the JSON string back into a Python object:

```python
import json

research_data = json.loads(row["research_data"])
```

The result is now a Python dictionary:

```python
print(type(research_data))
```

Output:

```python
<class 'dict'>
```

Access values normally:

```python
print(research_data["company"])
```

Output:

```text
Acme
```

---

## Example: Proposal Sections

AI-generated proposal sections:

```python
sections = {
    "executive_summary": "...",
    "scope": "...",
    "pricing": "..."
}
```

Store:

```python
json.dumps(sections)
```

Retrieve:

```python
sections = json.loads(row["sections"])
```

Access:

```python
sections["pricing"]
```

---

## Helper Functions

To avoid repeating serialization logic throughout the codebase:

```python
import json


def to_json(data):
    return json.dumps(data)


def from_json(data):
    return json.loads(data) if data else None
```

Usage:

```python
cursor.execute(
    """
    UPDATE proposals
    SET research_data = ?
    WHERE id = ?
    """,
    (
        to_json(research_data),
        proposal_id,
    ),
)
```

Read:

```python
research_data = from_json(row["research_data"])
```

---

## Recommendation

For the Proposal Agent, store the following fields as JSON:

- `parsed_data`
- `research_data`
- `retrieved_context`
- `sections`
- `review`

This allows complex structured data to be persisted in SQLite while remaining easy to work with in Python.
