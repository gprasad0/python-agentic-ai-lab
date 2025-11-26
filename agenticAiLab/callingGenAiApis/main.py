from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx
import time


def handlegenAI():
    load_dotenv(override=True)
    geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
    options = ["business", "technology", "healthcare", "finance", "education"]
    statments = []

    # messages =  [{"role": "user", "content": "Pick a business area that might be worth exploring for an agentic ai oppurtunity"}]
    # client = OpenAI(
    #     api_key=geminiApiKey,
    #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    # )
    # response = client.chat.completions.create(
    #     model="gemini-2.5-flash",
    #     messages=messages
    # )
    # answer =response.choices[0].message
    # print(answer)
    # for more info about httpx and asyncio read the docs in pythonLab/docs/async/asyncHttpx.md
    for option in options:
        print(f"Sending request for option: {option}")
        businessStatement = f"Pick a business area that might be worth exploring for an agentic ai oppurtunity in this field:{option}"
        messages = [{"role": "user", "content": businessStatement}]
        client = OpenAI(
            api_key=geminiApiKey,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        start = time.time()
        response = client.chat.completions.create(
            model="gemini-2.5-flash", messages=messages
        )
        end = time.time()
        print("Response received in:", round(end - start, 2), "seconds")

        statments.append(response.choices[0].message.content)

    print(statments)


if __name__ == "__main__":
    handlegenAI()
