from dotenv import load_dotenv
import os
from agents import Agent, Runner, Trace, function_tool
import asyncio
from pprint import pprint
import requests

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")

agentBehavior = [
    {
        "name": "codingAgent",
        "instructions": "You are a coding agent. Help with coding related tasks.",
    },
    {
        "name": "travelAgent",
        "instructions": "You are a travel agent. Help with travel related tasks.",
    },
    {
        "name": "healthAgent",
        "instructions": "You are a health agent. Help with health related tasks.",
    },
]


def createSpecializedAgent(agentName, agentInstructions):
    agent = Agent(name=agentName, instructions=agentInstructions, model=geminiLlmModel)
    return agent


def speicializedTools():
    tools = []
    for agent in agentBehavior:
        specializedAgent = createSpecializedAgent(agent["name"], agent["instructions"])
        specializedAgentAsTool = specializedAgent.as_tool(
            tool_name=agent["name"] + "Tool",
            tool_description="A tool to handle requests related to " + agent["name"],
        )
        tools.append(specializedAgentAsTool)
    return tools


@function_tool
async def sendNotification(notificationContent: str):
    """
    Send a notification to laptop with the content.
    """
    response = requests.post(
        "https://ntfy.sh/acer123",
        data=notificationContent,
        headers={"Title": "Task Success"},
    )
    return {"status": "successs"}


async def handoffMethod(input: str):
    handOffAgentInstructions = "You are an agent that will determine which specialized tool can be best used to handle the incoming request. Once the tool gives the data back, you need to handoff this data to the sendNotification tool to send a notification to the laptop"
    handOffAgent = Agent(
        name="handOffAgent",
        instructions=handOffAgentInstructions,
        tools=[*speicializedTools(), sendNotification],
        model=geminiLlmModel,
    )
    result = await Runner.run(
        handOffAgent,
        input=input,
    )
    return result


runHandOff = asyncio.run(
    handoffMethod("I want to go to Paris next month and I need help with the planning")
)
