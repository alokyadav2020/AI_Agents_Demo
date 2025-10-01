from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)


def return_google_client():
   

    google_api_key = os.getenv('GOOGLE_API_KEY')
    # GROQ_BASE_URL = "https://api.groq.com/openai/v1"
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    google_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)

    return google_client