from dotenv import load_dotenv
import os
import asyncio
import gradio as gr
from openai import AsyncOpenAI
from pypdf import PdfReader
from pydantic import BaseModel

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=geminiApiKey,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
name = "Ed Donner"


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


def linkedin():
    reader = PdfReader(f"{os.getenv('LINKEDIN_PDF')}/linkedin.pdf")
    pdfText = ""
    for page in reader.pages:
        pdfText += page.extract_text() + "\n"
    return pdfText


def summary():
    with open(f"{os.getenv('SUMMARY_TEXT')}/summary.txt", "r") as file:
        fileContent = file.read()
    return fileContent


system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so. Give short answers to keep down the token usage."

system_prompt += (
    f"\n\n## Summary:\n{summary()}\n\n## LinkedIn Profile:\n{linkedin()}\n\n"
)
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."


evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {name} and is representing {name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {name} in the form of their summary and LinkedIn details. Here's the information:"

evaluator_system_prompt += (
    f"\n\n## Summary:\n{summary()}\n\n## LinkedIn Profile:\n{linkedin()}\n\n"
)
evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."


async def evaluate(message, history, agent_response) -> Evaluation:
    user_prompt = (
        f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    )
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += (
        f"Here's the latest response from the Agent: \n\n{agent_response}\n\n"
    )
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
    messages = [
        {"role": "system", "content": evaluator_system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    print(f"Evaluator Messages: {messages}", flush=True)
    response = await client.chat.completions.parse(
        model="gemini-2.5-flash",
        messages=messages,
        response_format=Evaluation,  # synchronous call
    )
    print(f"Evaluator Respons: {response}", flush=True)
    return response.choices[0].message.parsed


def rerun():
    return None


async def chat(message, history):
    print(f"histroy===>{history}", flush=True)
    messages = (
        [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        + history
        + [
            {"role": "user", "content": message},
        ]
    )

    response = await client.chat.completions.create(
        model="gemini-2.5-flash", messages=messages
    )
    evaluatedContent = await evaluate(
        message, history, response.choices[0].message.content
    )
    print(f"Evaluation Result: {evaluatedContent}", flush=True)
    if evaluatedContent.is_acceptable:
        return response.choices[0].message.content
    else:
        return f"Response by LLM was not correct: {evaluatedContent.feedback}"


# if __name__ == "__main__":
#     asyncio.run(chat())
