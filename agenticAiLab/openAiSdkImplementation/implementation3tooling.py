from dotenv import load_dotenv
import os
from agents import Agent, Runner, Trace, function_tool
import asyncio
import requests

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")

agent1 = Agent(
    name="joker1",
    instructions="You are a joker. Tell a joke in one sentence.",
    model="litellm/gemini/gemini-2.5-flash",
)
agent2 = Agent(
    name="joker2",
    instructions="You are a joker. Tell a joke in one sentence.",
    model="litellm/gemini/gemini-2.5-flash",
)
evaluationAgent = Agent(
    name="jokeEvaluator",
    instructions="You are a joke evaluator. Evaluate the jokes from the payload and tell which one is better and why.",
    model="litellm/gemini/gemini-2.5-flash",
)


@function_tool
def sendNotificationToLaptop(jokeEvaluationResult: str):
    """
    Send a notification to laptop with the joke evaluation result.
    """
    response = requests.post(
        "https://ntfy.sh/acer123",
        data=jokeEvaluationResult,
        headers={"Title": "Task Success"},
    )
    return {"status": "successs"}


print("tool1==> ", agent1)
tool1 = agent1.as_tool(
    tool_name="jokeTool", tool_description="A tool to get a joke from joker1"
)
tool2 = agent2.as_tool(
    tool_name="jokeTool", tool_description="A tool to get a joke from joker2"
)

total_tools = [tool1, tool2, sendNotificationToLaptop]


async def evaluateAndSendJoke():
    result = await Runner.run()
