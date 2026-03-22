import os

from dotenv import load_dotenv
from openai import OpenAI
import requests

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize the OpenAI client
llm_client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
print("OpenAI client initialized successfully.")

# System prompt is hidden from the user and is used to set the behavior of the assistant. User prompt is the input from the user. Both are sent to the model to generate a response.


def get_weather(location):
    url = f"https://wttr.in/{location}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Sorry, I couldn't fetch the weather data at the moment."


print(get_weather("noida"))
