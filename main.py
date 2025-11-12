from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)
geminiApiKey = os.getenv('GOOGLE_GEMINI_API_KEY')
print(geminiApiKey)