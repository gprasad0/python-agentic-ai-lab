# Asyncio Complete Guide (with Explanations)

This guide explains asyncio from first principles, with explanations,
mental models, and examples.

This is designed for:

- Python modules
- Notebooks (Cursor / Jupyter)
- uv package management
- Real-world async usage (httpx, APIs, LLMs, Gradio)

---

# Table of Contents

1.  What is Asyncio
2.  Why Asyncio Exists
3.  Sync vs Async (DEEP explanation)
4.  The Event Loop (CORE CONCEPT)
5.  Coroutines Explained
6.  async and await Explained
7.  Running Async Code
8.  Tasks Explained
9.  asyncio.gather Explained
10. create_task Explained
11. Blocking vs Non-blocking
12. HTTP Requests with httpx
13. Notebook vs Python Script
14. Error Handling
15. Cancellation
16. Async Context Managers
17. Async Iterators
18. Best Practices
19. Common Mistakes
20. JavaScript Comparison
21. Mental Model Summary
22. Real-world Production Pattern

---

# 1. What is Asyncio

Asyncio is a library for writing concurrent programs using a single
thread.

KEY IDEA:

Asyncio allows your program to work on multiple things at once while
waiting.

IMPORTANT:

Asyncio is NOT parallelism.

It is concurrency.

Concurrency means:

Switch between tasks while waiting.

---

# 2. Why Asyncio Exists

Problem:

Normal code blocks.

Example:

    time.sleep(5)

Nothing else can run.

Program freezes.

Async solves this.

Instead of blocking, async pauses and allows other tasks to run.

---

# 3. Sync vs Async (DEEP explanation)

Sync code:

    download file A
    wait

    download file B
    wait

Total time = 10 seconds

Async code:

    start download A
    start download B
    wait both

Total time = 5 seconds

Explanation:

Async overlaps waiting time.

---

# 4. The Event Loop (CORE CONCEPT)

This is the MOST IMPORTANT concept.

The event loop is the engine that runs async code.

It does:

- starts tasks
- pauses tasks
- resumes tasks

Example:

    asyncio.run(main())

This creates event loop.

Without event loop:

Async code does nothing.

---

# 5. Coroutines Explained

Coroutine = async function

Example:

    async def hello():
        print("hello")

Calling:

    hello()

Does NOT run it.

It creates coroutine object.

Explanation:

Coroutines must be executed by event loop.

---

# 6. async and await Explained

await pauses coroutine.

Example:

    await asyncio.sleep(5)

Explanation:

Instead of blocking, coroutine pauses.

Event loop runs other tasks.

This is the heart of async.

---

# 7. Running Async Code

In Python script:

    asyncio.run(main())

Explanation:

Creates event loop Runs coroutine Closes event loop

In notebook:

    await main()

Explanation:

Notebook already has event loop.

---

# 8. Tasks Explained

Task = scheduled coroutine

Example:

    task = asyncio.create_task(fn())

Explanation:

This tells event loop:

Run this coroutine concurrently.

---

# 9. asyncio.gather Explained

Used to run multiple coroutines.

Example:

    await asyncio.gather(a(), b())

Explanation:

Runs both concurrently.

Waits for both.

---

# 10. create_task Explained

create_task starts coroutine immediately.

Example:

    asyncio.create_task(fn())

Explanation:

Runs in background.

---

# 11. Blocking vs Non-blocking

Blocking example:

    time.sleep(5)

Explanation:

Entire program stops.

Non blocking:

    await asyncio.sleep(5)

Explanation:

Only coroutine pauses.

Other tasks continue.

---

# 12. HTTP Requests with httpx

IMPORTANT:

requests blocks async.

Use httpx.

Example:

    async with httpx.AsyncClient() as client:
        await client.get(url)

Explanation:

httpx works with event loop.

Allows concurrency.

---

# 13. Notebook vs Python Script

Notebook:

Event loop exists.

Script:

You must create event loop.

---

# 14. Error Handling

Example:

    try:
        await fn()
    except Exception:
        pass

Explanation:

Works same as sync code.

---

# 15. Cancellation

Example:

    task.cancel()

Explanation:

Stops coroutine.

---

# 16. Async Context Managers

Example:

    async with client:

Explanation:

Used for async resources.

---

# 17. Async Iterators

Example:

    async for item in iterator:

Explanation:

Used for streaming data.

---

# 18. Best Practices

Use async libraries.

Avoid blocking calls.

---

# 19. Common Mistakes

Mistake:

Calling async function without await.

Example:

    fn()

Explanation:

Nothing runs.

---

# 20. JavaScript Comparison

Python:

gather

JavaScript:

Promise.all

---

# 21. Mental Model Summary

Async = cooperative multitasking

Event loop = manager

await = pause point

---

# 22. Real-world Production Pattern

Example:

    async with httpx.AsyncClient() as client:

        results = await asyncio.gather(

            client.get(url1),
            client.get(url2),
            client.get(url3),

        )

Explanation:

This runs HTTP calls concurrently.

This is the most common async pattern.

---

END
