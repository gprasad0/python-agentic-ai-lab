# Type Hints in Production Python

## One-Line Description

Learn how type hints create reliable, maintainable, and production-ready AI systems by making data contracts explicit.

---

# Why This Matters for FDE Roles

Forward Deployed Engineers spend much more time integrating systems than writing algorithms.

A typical AI workflow might involve:

- API requests
- Database queries
- Vector search results
- LLM outputs
- Workflow orchestration

Type hints ensure that every component agrees on what data is being passed and returned.

Without types, bugs often appear only at runtime.

With types, many errors are caught before deployment.

---

# Core Concept

Type hints define the expected shape of inputs and outputs.

Example:

```python
def calculate_score(score: int) -> int:
    return score * 10
```

This tells both developers and tooling:

- Input must be an integer
- Output will be an integer

---

# TypeScript Analogy

JavaScript:

```javascript
function createProposal(data) {
  return data.name;
}
```

TypeScript:

```typescript
type Prospect = {
  name: string;
  company: string;
};

function createProposal(data: Prospect): string {
  return data.name;
}
```

Production Python uses the same idea:

```python
def create_proposal(
    prospect: Prospect
) -> str:
    return prospect.name
```

---

# Using Pydantic Models

Instead of passing raw dictionaries, define explicit models.

```python
from pydantic import BaseModel


class CompanyResearch(BaseModel):
    company: str
    industry: str
```

Usage:

```python
def generate_proposal(
    research: CompanyResearch
) -> str:
    ...
```

Now every developer knows exactly what data is expected.

---

# AgentsFlo Example

## Lead Model

```python
from pydantic import BaseModel


class Lead(BaseModel):
    name: str
    company: str
    email: str
```

---

## Research Result

```python
from pydantic import BaseModel


class ResearchResult(BaseModel):
    company: str
    industry: str
    summary: str
```

---

## Proposal Response

```python
from pydantic import BaseModel


class ProposalResponse(BaseModel):
    proposal: str
    confidence: float
```

---

# Service Function Contracts

Research service:

```python
async def research_company(
    lead: Lead
) -> ResearchResult:
    ...
```

Proposal service:

```python
async def generate_proposal(
    research: ResearchResult
) -> ProposalResponse:
    ...
```

Every function clearly communicates:

- What it needs
- What it returns

---

# Typing Collections

List of strings:

```python
companies: list[str]
```

List of models:

```python
leads: list[Lead]
```

Dictionary:

```python
research: dict[str, str]
```

---

# Optional Values

Modern Python:

```python
linkedin_url: str | None
```

Equivalent older syntax:

```python
from typing import Optional

linkedin_url: Optional[str]
```

Prefer:

```python
str | None
```

for Python 3.10+.

---

# FastAPI Integration

FastAPI uses type hints for:

- Validation
- Serialization
- OpenAPI generation
- Swagger documentation

Example:

```python
@app.post("/research")
async def research_company(
    request: ResearchRequest
) -> ResearchResponse:
    ...
```

FastAPI automatically understands the request and response shapes.

---

# IDE Benefits

Type hints enable:

- Autocomplete
- Static analysis
- Refactoring support
- Error detection before runtime

Example:

```python
research.company
research.industry
research.summary
```

instead of guessing field names.

---

# Production Gotchas

### Using Any Everywhere

Bad:

```python
from typing import Any

data: Any
```

This removes most of the benefits of typing.

---

### Returning Raw Dictionaries

Bad:

```python
return {
    "summary": summary,
    "confidence": confidence
}
```

Better:

```python
return SummaryResponse(
    summary=summary,
    confidence=confidence
)
```

---

### Missing Return Types

Bad:

```python
def generate():
    ...
```

Better:

```python
def generate() -> ProposalResponse:
    ...
```

Always specify return types.

---

### Mixing Dictionaries and Models

Avoid:

```python
proposal["title"]
proposal.company
proposal["budget"]
```

Use a consistent model-driven approach.

---

# What I Built in AgentsFlo

- [ ] Created Lead model
- [ ] Created ResearchResult model
- [ ] Created ProposalResponse model
- [ ] Added typed service functions
- [ ] Added response models to FastAPI endpoints

Notes:

---

---

---

---

# Further Reading

- Pydantic Documentation
- FastAPI Type System
- Python Typing Documentation
- mypy Static Type Checker
- PEP 484 Type Hints
