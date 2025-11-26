from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx
import time

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=geminiApiKey,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


async def call_gemini_api(option):
    businessSTatement = f"Pick a business area that might be worth exploring for an agentic ai oppurtunity in this field:{option}"
    messages = [{"role": "user", "content": businessSTatement}]
    response = await client.chat.completions.create(
        model="gemini-2.5-flash", messages=messages
    )
    return response.choices[0].message.content


async def handlegenAI():
    options = ["business", "technology", "healthcare", "finance", "education"]
    tasks = [call_gemini_api(option) for option in options]
    results = await asyncio.gather(*tasks)  # * is an unpacking operator
    # for more info about httpx and asyncio read the docs in pythonLab/docs/async/asyncHttpx.md
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(handlegenAI())
