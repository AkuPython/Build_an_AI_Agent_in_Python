import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model="gemini-2.0-flash-001"

if len(sys.argv) < 2:
    print('Usage:\nmain.py "<prompt string>"')
    exit(1)

verbose = False
if "--verbose" in sys.argv:
    verbose = True

user_prompt = sys.argv[1]
if verbose:
    print("User prompt:", user_prompt, "\n")

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

resp = client.models.generate_content(model=model, contents=messages)

print(resp.text)

if resp.usage_metadata is not None and verbose:
    print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
    print("Response tokens:", resp.usage_metadata.candidates_token_count)
elif verbose:
    print("Couldn't get usage metadata")


