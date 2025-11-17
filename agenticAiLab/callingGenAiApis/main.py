from openai import OpenAI
from dotenv import load_dotenv
import os

def handlegenAI():
    load_dotenv(override=True)
    geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
    messages =  [{"role": "user", "content": "Pick a business area that might be worth exploring for an agentic ai oppurtunity"}]
    client = OpenAI(
        api_key=geminiApiKey,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )
    answer =response.choices[0].message
    print(answer)

if __name__ == "__main__": 
  handlegenAI()