from dotenv import load_dotenv
import os
import httpx
from agents import (
    Agent,
    Runner,
    trace,
    function_tool,
    input_guardrail,
    GuardrailFunctionOutput,
)
from pydantic import BaseModel
import httpx
from pprint import pprint
import asyncio

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")


@function_tool
async def sendNotification(message: str):
    """
    Use this tool to send the final selected email to the laptop notification system.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post("https://ntfy.sh/acer123", data=message)
    return {"status": "success"}


sendAgent = Agent(
    name="Sending Agent",
    instructions="You are an agent that receives a draft email. You make that email more concise, into 60 characters and use  sendNotification tool to send the concise draft to the laptop as a notification",
    tools=[sendNotification],
    model=geminiLlmModel,
)


@function_tool
async def emailAgent1tool(input: str):
    """
     You are a sales agent working for ComplAI, \
     a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
     You write very unprofessional and rude emails.It should only have 100 characters
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
        "description": "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails.It should only have 100 characters",
    },
    {
        "name": "emailAgent3",
        "description": "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response.It should only have 100 characters",
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
        agentTool = agent.as_tool(
            tool_name=agents["name"] + "tool",
            tool_description="A tool that creates an email response according to "
            + agents["name"],
        )
        emailAgents.append(agentTool)
    return emailAgents


tools = [emailAgent1tool, *createSalesAgentsTool(agentInstructions)]


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
    result = await Runner.run(guardRailAgent, message, context=ctx.context)
    is_name_in_user_input = result.final_output.is_name_in_user_input
    return GuardrailFunctionOutput(
        output_info={"found_name": result.final_output},
        tripwire_triggered=is_name_in_user_input,
    )


salesManagerInstructions = (
    "You are a sales manager. "
    "Run all email tools to generate multiple email drafts. "
    "Compare the drafts and choose the best one. "
    "Then handoff to the sendAgent agent to send notification"
)


sales_manager = Agent(
    name="salesManagerAgent",
    instructions=salesManagerInstructions,
    tools=tools,
    handoffs=[sendAgent],
    input_guardrails=[guardRail_against_name],
    model=geminiLlmModel,
)


async def runSalesManager(input):
    with trace("sales-email-system"):
        salesAgent = await Runner.run(sales_manager, input)
    return salesAgent.final_output


emailerAgent = asyncio.run(
    runSalesManager(
        "Send out a cold sales email addressed to Dear CEO from Head of Business Development"
    )
)
