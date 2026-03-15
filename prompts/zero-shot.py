import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize the OpenAI client
llm_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# System prompt is hidden from the user and is used to set the behavior of the assistant. User prompt is the input from the user. Both are sent to the model to generate a response.

SYSTEM_PROMPT = (
    """Your name is Dhurandhar. You always answer questions related to coding only"""
)

USER_PROMPT = input(">")

# List of messages to be sent to the model
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": USER_PROMPT},
]


response = llm_client.chat.completions.create(
    model="gemini-2.5-flash", messages=messages
)

print("Response from Gemini:")
print(response.choices[0].message.content)
