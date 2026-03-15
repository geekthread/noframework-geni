from openai import OpenAI

# Ollama serves a local OpenAI-compatible API on port 11434.
# Change MODEL to match your `ollama list` output, e.g. "gemma3:4b"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "gemma:2b"


def main():
    # Ollama doesn't need a real key, but the OpenAI client requires a non-empty string
    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
    print(f"Local Gemma client initialized (model: {MODEL}).")

    msgArray = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    response = client.chat.completions.create(
        model=MODEL, messages=msgArray, max_tokens=10
    )

    print("Response from Gemma:")
    print(response.choices[0].message.content)

    # Lets give some autonomy to the assistant
    prompt = "Ask me a question about Fair Value Gaps in trading to check my understanding of the concept."
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    print("Response from Gemma:")
    print(resp.choices[0].message.content)

    # Let LLM answer the question it just asked
    follow_up_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": resp.choices[0].message.content},
        ],
    )

    print("Follow-up response from Gemma:")
    print(follow_up_response.choices[0].message.content)


if __name__ == "__main__":
    main()
