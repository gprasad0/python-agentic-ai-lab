ASYNCIO and HTTPX

- asyncio is a event loop / concurrency manager not an HTTP client like fetch in JS or httpx in Python.

You need both:

asyncio → for async/concurrent execution

An HTTP library → to actually perform the network call

- httpx is a a http library like axios that lets you do non blocking api requests . Something like
  promise.all

Version 1 with both httpx and asyncio

```
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

Version 2 with just httpx

```
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
```

Both versions behave the SAME in speed.
You are awaiting each request one by one.

So the async code is still sequential.

Equivalent to JS:

```
for (const url of urls) {
  const res = await fetch(url)   // waits here
}
```

**When async becomes powerful (the real difference)**

The async version only becomes faster when you do parallel execution:

```
tasks = [client.get(url) for url in urls]
results = await asyncio.gather(*tasks)
```

Now it becomes equal to:

```
await Promise.all(urls.map(url => fetch(url)))
```

That’s the real power.

**When should YOU use which?**

Use this:

✅ Normal scripts / APIs / automation

```
with httpx.Client() as client:
for url in urls:
```

🚀 Scraping / bulk requests / 50+ calls

```
async with httpx.AsyncClient()...
await asyncio.gather(...)
```

**async is only better when you use concurrency. Otherwise, it’s just more complicated.**

EXAMPLE CODE :

```
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
**Creating async client**
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
    results = await asyncio.gather(*tasks)   //* is a spread operator in python

    for prompt, answer in results:
        print("\nPROMPT:", prompt)
        print("ANSWER:", answer)

asyncio.run(main())
```

EXPLANATION FOR THE EXAMPLE CODE :

This is an asynchronous, parallel API caller.

- Creates multiple tasks
- Sends them at the same time
- Waits for all of them to finish
- Prints the results

AsyncOpenAI = async version of OpenAI client

tasks = [call_gpt(p) for p in prompts] - > This creates a list like:

```
    [
  coroutine(call_gpt(prompt1)),
  coroutine(call_gpt(prompt2)),
  coroutine(call_gpt(prompt3)),
  coroutine(call_gpt(prompt4))
    ]
'''

**What does the * do here?**
It converts this:
asyncio.gather(tasks)

Into this:
```

asyncio.gather(task1, task2, task3, task4)

```
Required because gather() expects multiple arguments, not a single list.
JS equivalent:
await Promise.all([...tasks])

Python equivalent logic:
await asyncio.gather(task1, task2, task3, task4)
```

```

```
