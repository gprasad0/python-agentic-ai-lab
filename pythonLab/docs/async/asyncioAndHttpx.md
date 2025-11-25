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

tasks = [client.get(url) for url in urls]
results = await asyncio.gather(\*tasks)

Now it becomes equal to:

await Promise.all(urls.map(url => fetch(url)))

That’s the real power.

**When should YOU use which?**

Use this:

✅ Normal scripts / APIs / automation
with httpx.Client() as client:
for url in urls:
...

🚀 Scraping / bulk requests / 50+ calls
async with httpx.AsyncClient()...
await asyncio.gather(...)

**async is only better when you use concurrency. Otherwise, it’s just more complicated.**
