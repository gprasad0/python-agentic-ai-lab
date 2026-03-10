from dotenv import load_dotenv
import os
from agents import Agent, Runner, Trace, function_tool
import asyncio
import requests

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")
agent1 = Agent(
    name="joker1",
    instructions="You are a joker. Tell a joke in one sentence about engineers",
    model=geminiLlmModel,
)
agent2 = Agent(
    name="joker2",
    instructions="You are a joker. Tell a joke in one sentence about doctors",
    model=geminiLlmModel,
)


@function_tool
async def sendNotificationToLaptop(jokeEvaluationResult: str):
    """
    Send a notification to laptop with the joke evaluation result.
    """
    response = requests.post(
        "https://ntfy.sh/acer123",
        data=jokeEvaluationResult,
        headers={"Title": "Task Success"},
    )
    return {"status": "successs"}


tool1 = agent1.as_tool(
    tool_name="engineerJokeTool",
    tool_description="A tool to tell a joke about engineers",
)
tool2 = agent2.as_tool(
    tool_name="doctorJokeTool", tool_description="A tool to tell a joke about doctors"
)

total_tools = [tool1, tool2, sendNotificationToLaptop]

evaluationAgent = Agent(
    name="jokeEvaluator",
    instructions="You are a joke evaluator. Evaluate jokes",
    tools=total_tools,
    model=geminiLlmModel,
)


async def evaluateAndSendJoke():
    result = await Runner.run(
        evaluationAgent,
        "Evaluate the jokes from the tools given. Use sendNotificationToLaptop tool to send a notification to the laptop with the joke you seem to like better and why",
    )
    return result


evaluationResult = asyncio.run(evaluateAndSendJoke())
