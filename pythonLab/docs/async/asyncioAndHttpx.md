# ASYNCIO and HTTPX

---

## What is asyncio and httpx

- `asyncio` is an **event loop / concurrency manager**, not an HTTP
  client like `fetch` in JS or `httpx` in Python.

You need both:

- `asyncio` → for async / concurrent execution\
- An HTTP library → to actually perform the network call

---

- `httpx` is an HTTP library like `axios` that lets you do
  **non-blocking API requests**. Something like `Promise.all`.

---

# Version 1 with both httpx and asyncio

```python
import asyncio
import httpx

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/2"
    ]

    async with httpx.AsyncClient() as client:
        for url in urls:
            print("Calling:", url)
            response = await client.get(url)
            print(response.json())

asyncio.run(main())
```

---

# Version 2 with just httpx

```python
import httpx

urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3",
]

with httpx.Client() as client:
    for url in urls:
        response = client.get(url)
        print(response.json())
}
```

---

# Both versions behave the SAME in speed

You are awaiting each request one by one.

So the async code is still sequential.

Equivalent to JS:

```javascript
for (const url of urls) {
  const res = await fetch(url);
}
```

---

# When async becomes powerful (the real difference)

The async version only becomes faster when you do parallel execution:

```python
tasks = [client.get(url) for url in urls]
results = await asyncio.gather(*tasks)
```

Now it becomes equal to:

```javascript
await Promise.all(urls.map((url) => fetch(url)));
```

---

# When should YOU use which?

Use this:

Normal scripts / APIs / automation

```python
with httpx.Client() as client:
    for url in urls:
        ...
```

Scraping / bulk requests / 50+ calls

```python
async with httpx.AsyncClient() as client:
    await asyncio.gather(...)
```

---

# Example Code

```python
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=geminiApiKey,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

prompts = [
    "Pick a business area for agentic AI",
    "List 3 pain points in that area",
    "Suggest a startup idea",
    "Monetization strategy?"
]

async def call_gpt(prompt):
    messages = [{"role": "user", "content": prompt}]

    response = await client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )

    return prompt, response.choices[0].message.content


async def main():

    tasks = [call_gpt(p) for p in prompts]

    results = await asyncio.gather(*tasks)

    for prompt, answer in results:
        print("\nPROMPT:", prompt)
        print("ANSWER:", answer)


asyncio.run(main())
```

---

# Explanation

This is an asynchronous parallel API caller.

Creates multiple tasks\
Sends them at same time\
Waits for all\
Prints results

---

# Spread Operator

```python
await asyncio.gather(task1, task2, task3)
```

Equivalent JS

```javascript
await Promise.all([...tasks]);
```

---
