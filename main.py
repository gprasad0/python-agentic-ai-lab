from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
print(geminiApiKey)


def handlegenAI():
    print("hi")
    messages = [{"role": "user", "content": "Something here"}]
    client = OpenAI(
        api_key=geminiApiKey,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "user", "content": "Pick a business area that might be worth exploring for an agentic ai oppurtunity"},
        ],
    )
    answer =response.choices[0].message
    print(answer)



handlegenAI()
