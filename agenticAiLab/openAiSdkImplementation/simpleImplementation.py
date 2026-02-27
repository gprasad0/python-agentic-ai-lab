from dotenv import load_dotenv
import os
from agents import Agent, Runner, Trace
import asyncio
from agents.providers import GoogleProvider

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
agent = Agent(
    name="fortune teller",
    instructions="You are a fortune teller. Tells fortune in one sentence in a riddle.",
    model="gemini-2.5-flash",
    provider=GoogleProvider(),
)


async def callAgent(input):
    fortuneTellerAgent = await Runner.run(agent, input)
    print(f"response==> {fortuneTellerAgent.response}")
    return fortuneTellerAgent.response


asyncio.run(callAgent("Tell me my fortune for today"))
