from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, Trace, function_tool, OpenAIChatCompletionsModel
import os
import httpx
import json
from pprint import pprint
import asyncio

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("GEMINI_BASE_URL")


@function_tool
async def callEmailAgent(input: str):
    """
    A tool that can be used for a cold email. It takes in the input paramter for teh cold email context and gives back the email data
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
        return response["choices"][0]["message"]["content"]


@function_tool
async def callTravelAgent(input: str):
    """
    A tool to get the travel recommendation from the Gemini model based on the user input
    """
    gemini_client = AsyncOpenAI(base_url=geminiLlmModel, api_key=geminiApiKey)
    gemini_model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash", openai_client=gemini_client
    )
    agent = Agent(
        name="geminiAgent",
        instructions="You are a travelguide. Help the user with travel recommendations and then send a notification to the laptop with the recommendation using the sendNotificationToLaptop tool",
        model=gemini_model,
        tools=[sendNotificationToLaptop],
    )
    travelAgent = await Runner.run(agent, input)
    return travelAgent.final_output


@function_tool
async def sendNotificationToLaptop(notification: str):
    """
    A tool to send notification to laptop using ntfy.sh
    """
    response = await httpx.post(
        "https://ntfy.sh/acer123",
        data=notification,
        headers={"Title": "Travel Recommendation"},
    )
    return {"status": "success"}


async def callTools():
    result = await Runner.run(
        Agent(
            name="mainAgent",
            instructions="You are an agent that detrmines which tool"
            " has to be used to handle the user request. You have access to two tools - callTravelAgent and callEmailAgent. Based on the user request, call the appropriate tool. If the tool  callEmailAgent is used, then take the input and then call the sendNotificationToLaptop tool to send a notification to the laptop with the email data received from callEmailAgent",
            tools=[callTravelAgent, callEmailAgent, sendNotificationToLaptop],
        ),
        "Plan a trip to Paris for me.",
    )
    return result


result = asyncio.run(callTools())
