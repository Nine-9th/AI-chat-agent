import json
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("no api key set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

message = response.choices[0].message
for tool_call in message.tool_calls:
    result_message = call_function(tool_call, verbose=args.verbose)
    if result_message["content"] == "":
        raise Exception("Function returned empty result")
    if args.verbose:
        print(f"-> {result_message['content']}")

if response.usage is None:
    raise RuntimeError("failed api request")
elif args.verbose:
    print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
    
