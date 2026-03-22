import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize the OpenAI client
llm_client = OpenAI()


# System prompt is hidden from the user and is used to set the behavior of the assistant. User prompt is the input from the user. Both are sent to the model to generate a response.
SYSTEM_PROMPT = """
You are an expert AI assitant that solves use queries using a structured reasoning workflow.

You must operrate in three steps:
1. Start

"""

USER_PROMPT = input(">")

# List of messages to be sent to the model
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": USER_PROMPT},
]


response = llm_client.chat.completions.create(model="gpt-4o-mini", messages=messages)

print("Response from Gemini:")
print(response.choices[0].message.content)
