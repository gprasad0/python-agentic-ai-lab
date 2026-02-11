from urllib import response
from dotenv import load_dotenv
import os
from numpy import rint
import requests
import gradio as gr
from pypdf import PdfReader
from openai import OpenAI
from pprint import pprint

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")


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


def record_user_details(email: str, name: str, notes: str):
    pushNotification(notes)
    return {
        "recorded": f"Recorded user details"
    }


def record_unknown_questions(questions: str):
    pushNotification(questions)
    return {
        "recorded": f"Recorded unknown question"
    }


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
        "additionalProperties": False,  # Whether extra (unspecified) fields are allowed in the input.
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

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_questions_json},
]

def get_tool_map():
    return{
        "record_user_details": record_user_details,
        "record_unknown_questions": record_unknown_questions
    }


class Agent:
    def __init__(self):
        self.openAiClient = OpenAI(
            api_key=geminiApiKey,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self.pdfText = readPdf()
        self.summaryText = readText()
        self.name = "Ed Donner"

    def systemPrompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_unknown_questions tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summaryText}\n\n## LinkedIn Profile:\n{self.pdfText}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt


{
  "id": "A-WLae7RKNnx4-EP1dvR-QU",
  "object": "chat.completion",
  "created": 1770775812,
  "model": "gemini-2.5-flash",
  "choices": [
    {
      "index": 0,
      "finish_reason": "tool_calls",
      "logprobs": null,
      "message": {
        "role": "assistant",
        "content": null,
        "refusal": null,
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [
          {
            "id": "function-call-9127675616511081436",
            "type": "function",
            "function": {
              "name": "record_unknown_questions",
              "arguments": {
                "questions": "ew"
              }
            }
          }
        ]
      }
    }
  ],
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 814,
    "total_tokens": 927,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  }
}



    def handleToolCalls(self, tool_calls):
        records = []
        for tool in tool_calls:
            toolName = tool.function.name
            toolargumets = tool.function.arguments
            recorded_data = get_tool_map()[toolName](**toolargumets)
            records.append(recorded_data)

        return records

    def callGradio(self, user_input, chat_history):
        reply = user_input
        messages = [
            {"role": "system", "content": self.systemPrompt()},
            *chat_history,
            {"role": "user", "content": reply},
        ]

        # response = self.openAiClient.chat.completions.create(
        #     model="gemini-2.5-flash", messages=messages, tools=tools
        # )
        pprint(f"Response: {response}")
        # response = "tool_calls"
        if response.choices[0].finish_reason == "tool_calls":
            toolcalls = response.choices[0].message.tool_calls
            invoketoolCalls = self.handleToolCalls(toolcalls)

        return response.choices[0].message.content
        # return response.choices[0].message.content
