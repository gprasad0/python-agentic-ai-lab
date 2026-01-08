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


# if __name__ == "__main__":
#     text = readPdf()
#     print(text)
