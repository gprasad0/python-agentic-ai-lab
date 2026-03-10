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
import httpx

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")


@function_tool
async def sendNotification(message: str):
    """
    A tool that sends the message input as the notification to the laptop
    """
    response = await httpx.post(
        "https://ntfy.sh/acer123",
    )
    async with httpx.AsyncClient() as client:
        response = await client.post("https://ntfy.sh/acer123", data=message)
        return {"status": "success"}


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


def createSalesAgentsTool(agentInstructions):
    emailAgents = []
    for agents in agentInstructions:
        agent = Agent(
            name=agents["name"],
            instructions=agents["description"],
            model=geminiLlmModel,
        )
        agent.as_tool(
            tool_name=agents["name"] + "tool",
            tool_description="A tool that creates an email response according to "
            + agents["name"],
        )
        emailAgents.append(agent)
    return emailAgents


tools = [emailAgent1, *createSalesAgentsTool]


class NameCheckOutPut(BaseModel):
    is_name_in_user_input: bool
    name: str


guardRailAgent = Agent(
    name="guardrailAgent",
    instructions="You determine whether the user input has a name in it or not",
    output_type=NameCheckOutPut,
    model=geminiLlmModel,
)


@input_guardrail
async def guardRail_against_name(ctx, agent, message):
    result = Runner.run(guardRailAgent, message, context=ctx.context)
    is_name_in_user_input = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(
        output_info={"found_name": result.final_output},
        tripwire_triggered=is_name_in_user_input,
    )


salesManagerInstructions = (
    "Youre a sales manager.You will run the tools and get all the emails from it."
    "Then decide which email is best and the hand it off to the sendNotification tool who will send the notification "
)

sales_manager = Agent(
    name="salesManagerAgent",
    instructions=salesManagerInstructions,
    tools=tools,
    handoffs=[sendNotification],
)
