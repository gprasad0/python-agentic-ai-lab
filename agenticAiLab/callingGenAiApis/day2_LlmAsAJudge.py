from dotenv import load_dotenv
import os
import asyncio
import gradio as gr
from openai import AsyncOpenAI
from pypdf import PdfReader

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=geminiApiKey,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
name = "Ed Donner"


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


def evaluate():
    return None


def rerun():
    return None


async def chat(message, history):
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
    print(f"response===>{response}", flush=True)
    return response.choices[0].message.content


# if __name__ == "__main__":
#     asyncio.run(chat())
