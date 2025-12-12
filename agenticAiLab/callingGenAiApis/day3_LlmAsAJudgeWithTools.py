from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
pushoverUser = os.getenv("PUSHOVER_USER")
pushoverToken = os.getenv("PUSHOVER_TOKEN")
pushoverUrl = "https://api.pushover.net/1/messages.json"


def push(message):
    print(f"Sending push notification: {message}")
    payload = {"user": pushoverUser, "token": pushoverToken, "message": message}
    requests.post(pushoverUrl, data=payload)


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}


class Me:
    def __init__(self):
        self.name = "Guru"
        self.email = "guru@example.com"
        self.client = OpenAI(
            api_key=geminiApiKey,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    def callGradle(self):
        print("rsponse111")

        messages = [{"role": "user", "content": "Hello, how are you?"}]
        response = self.client.chat.completions.create(
            model="gemini-2.5-flash", messages=messages
        )
        print("rsponse", response.choices[0].message.content)
        return response.choices[0].message.content


# if __name__ == "__main__":
#     me = Me()


# record_user_details -> record unknown question ->
