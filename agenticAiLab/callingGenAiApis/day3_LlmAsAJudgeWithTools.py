from dotenv import load_dotenv
import os
import requests
import gradio as gr
from pypdf import PdfReader

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
        "https://ntfy.sh/acerLaptop8212",
        data=message,
        headers={"Title": "Task Success"},
    )
    print(f"Pushover response: {response.text}")
    data = response.json()
    return data.get("message")


# if __name__ == "__main__":
#     text = readPdf()
#     print(text)
