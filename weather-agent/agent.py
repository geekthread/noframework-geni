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
    

SYSTEM_PROMPT = """
You're an expert AI assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps to resolve the user query.
START: You start by understanding the user query and identifying the key components required to resolve it.
PLAN: You create a plan to resolve the user query by breaking it down into smaller steps and identifying the tools required for each step.
OUTPUT: You execute the plan by using the identified tools and providing the final output to the user.

Rules:
1. Always follow the START, PLAN and OUTPUT steps in order.
2. Use the tools available to you to resolve the user query.
3. If you encounter any issues while executing the plan, go back to the PLAN step and revise your plan accordingly.
4. Always provide the final output to the user after executing the plan.

Output Json Format:
{ "step" : "START/PLAN/OUTPUT", "reasoning": "Your reasoning for the current step", 
"tool": "The tool you used in this step (if any)", "output": "The output from the tool (if any)" }

Available Tools:
1. get_weather(location): This tool takes a location as input and returns the current weather for that location.


Example:User Query: What is the current weather in New York?
Response:
{ "step" : "START", "reasoning": "The user is asking for the current weather in New York. I need to use the get_weather tool to fetch this information.", "tool": "", "output": "" }

{ "step" : "PLAN", "reasoning": "I will use the get_weather tool with 'New York' as the input to fetch the current weather information.", "tool": "get_weather('New York')", "output": "" }

{ "step" : "OUTPUT", "reasoning": "I have fetched the current weather information for New York using the get_weather tool. Now I will provide this information to the user.", "tool": "", "output": "The current weather in New York is sunny with a temperature of 25°C." }


"""


msgs = [
    {"role": "system", "content": SYSTEM_PROMPT},
   
]

need_input = True

while True:
    if need_input:
        USER_PROMPT = input("> ")
        if USER_PROMPT.lower() in ("exit", "quit"):
            break
        msgs.append({"role": "user", "content": USER_PROMPT})
        need_input = False

    response = llm_client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=msgs)

    print ("""------------------Model Response------------------""")
    print("Inside loop after getting response from model")
    assistant_response = response.choices[0].message.content
    print(assistant_response)

    # Append the assistant response to the messages list for context in the next iteration
    msgs.append({"role": "assistant", "content": assistant_response})
    
   # print(msgs)

    # Convert the model's text response into a Python dictionary so we can read fields like "step" and "tool"
    response_json = eval(assistant_response)

    # If the model decided to use a tool (during PLAN step), run it and send the result back
    if response_json["step"] == "PLAN" and response_json["tool"] != "":
        # Actually execute the tool (e.g. get_weather('Delhi')) and get the real data
        tool_output = eval(response_json["tool"])
        print(f"Tool output: {tool_output}")
        # Feed the tool result back as a user message so the model can use it in the next step
        msgs.append({"role": "user", "content": f"Tool output: {tool_output}"})
      #  print(msgs)

    # If the model has given the final answer, ask the user for a new question
    if response_json["step"] == "OUTPUT":
        need_input = True
    
   
