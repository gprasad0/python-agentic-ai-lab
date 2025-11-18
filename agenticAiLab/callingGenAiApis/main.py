from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx


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
    for option in options:
        businessStatement = f"Pick a business area that might be worth exploring for an agentic ai oppurtunity in this field:{option}"
        statments.append(businessStatement)

    print(statments)


if __name__ == "__main__":
    handlegenAI()
