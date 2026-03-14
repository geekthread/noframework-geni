import os
from http import client

from dotenv import load_dotenv
from openai import OpenAI


def main():
    print("Hello from noframework!")
    load_dotenv(override=True)
    print("Environment variables loaded.")
    open_ai_key = os.getenv("OPEN_AI_KEY")
    print(
        f"OPEN_AI_KEY: {open_ai_key[:10]}..."
    )  # Print only the first 10 characters for security

    openai_client = OpenAI(api_key=open_ai_key)
    print("OpenAI client initialized.")
    print("OpenAI client is ready to use.")
    msgArray = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano", messages=msgArray, max_tokens=10
    )

    print("Response from OpenAI:")
    print(response.choices[0].message.content)

    # Lets give some autonomy to the assistant
    prompt = "Ask me a question about Fair Value Gaps in trading to check my understanding of the concept."
    resp = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    print("Response from OpenAI:")
    print(resp.choices[0].message.content)

    # Let LLM answer the question it just asked
    follow_up_response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": resp.choices[0].message.content},
        ],
    )

    print("Follow-up response from OpenAI:")
    print(follow_up_response.choices[0].message.content)


if __name__ == "__main__":
    main()
