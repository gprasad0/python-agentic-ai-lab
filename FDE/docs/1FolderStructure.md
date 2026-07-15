# Production Python Project Structure with uv

## One-Line Description

Learn how production Python applications are structured using uv, pyproject.toml, and the src layout pattern.

---

# Why This Matters for FDE Roles

Forward Deployed Engineers rarely build one-off scripts.

They build production systems that:

- Integrate with AI models
- Scale across teams
- Run in cloud environments
- Support long-term maintenance

A well-structured codebase makes AI applications easier to test, deploy, and extend.

---

# Core Concept

A common beginner mistake is placing all application logic inside a single file.

Bad:

```text
main.py
```

As the application grows:

```text
main.py -> 1500+ lines
```

This becomes difficult to maintain.

Production Python applications separate responsibilities into dedicated modules.

Recommended structure:

```text
agentsflo/

├── pyproject.toml
├── README.md
├── .env

├── src/
│   └── agentsflo/
│
│       ├── api/
│       ├── services/
│       ├── clients/
│       ├── core/
│       ├── workflows/
│       ├── models/
│       └── main.py
│
├── tests/
│
└── docs/
```

---

# Why Use the src Layout?

The src pattern prevents accidental imports from the local working directory.

Instead of importing local files directly, Python imports the package exactly as it would in production.

Benefits:

- Consistent imports
- Fewer deployment bugs
- Cleaner packaging
- Better CI/CD reliability

Example:

```text
src/
└── agentsflo/
```

---

# pyproject.toml

Think of pyproject.toml as Python's version of package.json.

Example:

```toml
[project]
name = "agentsflo"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi",
    "uvicorn",
    "openai",
    "langgraph"
]
```

This file manages:

- Dependencies
- Project metadata
- Build configuration
- Tooling configuration

---

# Using uv

Initialize project:

```bash
uv init agentsflo
```

Add dependencies:

```bash
uv add fastapi
uv add uvicorn
```

Add development dependencies:

```bash
uv add --dev pytest
```

Run application:

```bash
uv run uvicorn src.agentsflo.main:app --reload
```

Run tests:

```bash
uv run pytest
```

---

# Environment Configuration

Avoid hardcoding secrets.

Bad:

```python
OPENAI_API_KEY = "secret"
```

Use environment variables:

```env
OPENAI_API_KEY=your_key
DATABASE_URL=postgres_url
```

Load them using Pydantic Settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

# AgentsFlo Example

## API Route

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/proposal")
async def create_proposal():
    return await proposal_service.generate()
```

The route handles HTTP concerns only.

---

## Service Layer

```python
class ProposalService:

    async def generate(self):

        # Fetch company data
        # Generate proposal
        # Store result

        return {
            "status": "success"
        }
```

The service contains business logic.

---

# Separation of Responsibilities

## api/

Responsible for:

- Routes
- Request handling
- Response handling
- Authentication

---

## services/

Responsible for:

- Business logic
- AI workflows
- Data processing
- Retrieval pipelines

---

## clients/

Responsible for:

- OpenAI client
- Pinecone client
- PostgreSQL client
- Third-party integrations

---

## core/

Responsible for:

- Configuration
- Logging
- Exceptions
- Shared utilities

---

# Production Gotchas

### Putting Everything in main.py

Bad for maintenance and testing.

---

### Calling LLMs Directly from Routes

Bad:

```python
@app.post("/generate")
async def generate():
    await openai.chat.completions.create(...)
```

Move LLM calls into services.

---

### Scattered Environment Variables

Avoid:

```python
os.getenv(...)
```

across many files.

Use a centralized settings module.

---

### No Tests Folder

Create:

```text
tests/
```

from day one.

---

# What I Built in AgentsFlo

- [ ] Created src-based structure
- [ ] Added pyproject.toml
- [ ] Added FastAPI application
- [ ] Added settings configuration
- [ ] Added service layer
- [ ] Added tests folder

Notes:

---

---

---

---

# Further Reading

- uv Documentation
- FastAPI Documentation
- Pydantic Settings
- Python Packaging User Guide
- Hypermodern Python Project Structure
