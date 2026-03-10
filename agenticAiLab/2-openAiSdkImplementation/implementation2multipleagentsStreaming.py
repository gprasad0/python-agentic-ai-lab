from dotenv import load_dotenv
import os
from agents import Agent, Runner, Trace
import asyncio
from pprint import pprint
import json

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")


async def callMultipleAgents(input):
    agent1 = Agent(
        name="jokeAgent1",
        instructions="You are a joke agent. Tell a joke in one sentence.",
        model="litellm/gemini/gemini-2.5-flash",
    )
    agent2 = Agent(
        name="jokeAgent2",
        instructions="You are a joke agent. Tell a joke in one sentence.",
        model="litellm/gemini/gemini-2.5-flash",
    )
    agent3 = Agent(
        name="jokeEvaluator",
        instructions="You are a joke evaluator. Evaluate the jokes from the payload and tell which one is better and why.",
        model="litellm/gemini/gemini-2.5-flash",
    )
    jokeAgentResults = await asyncio.gather(
        Runner.run(agent1, input), Runner.run(agent2, input)
    )
    finalJokes = [result.final_output for result in jokeAgentResults]
    payload = json.dumps({"jokes": finalJokes})
    evaluatorAgent = Runner.run_streamed(agent3, payload)

    final_text = ""
    async for event in evaluatorAgent.stream_events():
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
            final_text += event.delta

        return final_text


bestJoke = asyncio.run(callMultipleAgents("Tell me a joke for today"))
