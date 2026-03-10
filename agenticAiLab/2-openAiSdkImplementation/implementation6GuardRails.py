from dotenv import load_dotenv
import os
import httpx
from agents import (
    Agent,
    Runner,
    Trace,
    function_tool,
    input_guardrail,
    GuardrailFunctionOutput,
)
from pydantic import BaseModel

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")


@function_tool
async def emailAgent1(input: str):
    """
    A tool that can be used for providing a cold email response. It gives a very salesly response and tries to push the user to buy the product
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


agentInstructions = [
    {
        "name": "emailAgent2",
        "description": "You are an agent that gives a vey funny email response.",
    },
    {
        "name": "emailAgent3",
        "description": "You are an agent that gives a very technical email response.",
    },
]


def createSalesAgents(agentInstructions):
    emailAgents = []
    for agents in agentInstructions:
        agent = Agent(name=agents["name"], instructions=agents["description"])
        agent.as_tool(
            tool_name=agents["name"] + "tool",
            tool_description="A tool that creates an email response according to "
            + agents["name"],
        )
        emailAgents.append(agent)
    return emailAgents


tools = [emailAgent1, *createSalesAgents]


class NameCheckOutPut(BaseModel):
    is_name_in_user_input: bool
    name: str


guardRailAgent = Agent(
    name="guardrailAgent",
    instructions="You determine whether the user input has a name in it or not",
    output_type=NameCheckOutPut,
)
