from dotenv import load_dotenv
import os
import gradio as gr
from pypdf import PdfReader

load_dotenv(override=True)


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


# if __name__ == "__main__":
#     text = readPdf()
#     print(text)
