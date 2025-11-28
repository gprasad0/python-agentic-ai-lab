from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx
import time

# PROMPT CHAINS CAN BE USED TO CHAIN MULTIPLE PROMPTS TOGETHER TO GET A MORE REFINED OUTPUT
# BELOW IS A PROMPT CHAINING WORFLOW
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
    businesResults = []
    for i, result in enumerate(results):
        businesResults.append({options[i]: result})
    messages = [
        {
            "role": "user",
            "content": f"tell me the best idea out of all these . I have given an array of objects that contains multiple ideas. Go through it and let me know the best one{businesResults}",
        }
    ]
    response = await client.chat.completions.create(
        model="gemini-2.5-flash", messages=messages
    )
    print("Final Idea from all the options:", response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == "__main__":
    asyncio.run(handlegenAI())
