from dotenv import load_dotenv
import os
import requests
import gradio as gr
from pypdf import PdfReader
from openai import OpenAI

load_dotenv(override=True)
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def readPdf():
    reader = PdfReader(f"{os.getenv('LINKEDIN_PDF')}/linkedin.pdf")
    pdfText = ""
    for page in reader.pages:
        pdfText = page.extract_text() + "\n"
    return pdfText


def readText():
    with open(f"{os.getenv('SUMMARY_TEXT')}/summary.txt", "r") as file:
        text = file.read()
    return text


def aboutUser():
    pdf = readPdf()
    text = readText()
    return f"{pdf}\n\n{text}"


def pushNotification(message: str):
    response = requests.post(
        "https://ntfy.sh/acer123",
        data=message,
        headers={"Title": "Task Success"},
    )
    print(f"Pushover response: {response.text}")


def record_user_details(email: str, name: str, notes: str):
    pushNotification(notes)
    return f"Recorded details for {name} with email {email}."


def record_unknown_questions(questions: str):
    pushNotification(questions)
    return f"Recorded unknown questions: {questions}"


record_user_details_json = {
    "name": "record_user_details",
    "description": "This tool records user details such as email, name and any extraneous notes",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of the user",
            },
            "name": {
                "type": "string",
                "description": "The name of the user, if provided",
            },
            "notes": {
                "type": "string",
                "description": "Any additional notes about the user",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_questions_json = {
    "name": "record_unknown_questions",
    "description": "This tool records any unknown questions asked by the user",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "string",
                "description": "The unknown questions asked by the user",
            },
        },
        "required": ["questions"],
        "additionalProperties": False,
    },
}

toolSchema = [
    record_user_details_json,
    record_unknown_questions_json,
]


class Agent:
    def __init__(self):
        self.openAiClient = OpenAI()
        self.pdfText = readPdf()
        self.summaryText = readText()
        self.name = "Ed Donner"

    def systemPrompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to a question, you must use the 'record_unknown_questions' tool to record the question. \
            If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summaryText}\n\n## LinkedIn Profile:\n{self.pdfText}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def handleToolCalls(self, tool_calls):
        return 1

    def callGradio(self, user_input, chat_history):
        reply = user_input
        print(f"User input: {user_input} chat history: {chat_history}", flush=True)
        if reply == "hi":
            return "hello"
        else:
            return "please say hi"
