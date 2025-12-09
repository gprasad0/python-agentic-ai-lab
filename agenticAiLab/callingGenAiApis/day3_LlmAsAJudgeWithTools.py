from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
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


if __name__ == "__main__":
    push("HEY")
