from dotenv import load_dotenv
import os
import asyncio
import gradio as gr
from pypdf import PdfReader

# Read pdf and test file
# add both these to a variable
# Create an evaluate method that evaluates the messages coming from the main GPT
# If evaluate is true, print passed evaluation
# else print failed evaluation and run a rerun method

load_dotenv(override=True)


def readPdf():
    reader = PdfReader(f"{os.getenv('LINKEDIN_PDF')}/linkedin.pdf")
    pdfText = ""
    for page in reader.pages:
        pdfText += page.extract_text() + "\n"
    print("PDF Text", pdfText)
    return pdfText


def readTextFile():
    with open(f"{os.getenv('SUMMARY_TEXT')}/summary.txt", "r") as file:
        fileContent = file.read()
    print("File Content:", fileContent)
    return fileContent


def run():
    pdfContent = readPdf()
    readTextFile()


if __name__ == "__main__":
    run()
