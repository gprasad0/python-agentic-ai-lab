from dotenv import load_dotenv

from agents import Agent, Runner, Trace, function_tool
import os
import httpx
import json
from pprint import pprint
import asyncio

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")


@function_tool
async def callOpenRouterAPi(input: str):
    """
    A tool to call the OpenRouter API with given input and return the response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": input,
                    }
                ],
                "reasoning": {"enabled": True},
            },
        )
        response = response.json()
        print("Response from OpenRouter API:")
        pprint(response)
        return response["choices"][0]["message"]["content"]


asyncio.run(callOpenRouterAPi("What is the capital of France?"))
