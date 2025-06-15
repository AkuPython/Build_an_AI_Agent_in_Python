import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.call_function import call_function

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


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

resp = client.models.generate_content(
    model=model,
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
    )
)

function_calls = resp.function_calls
call_results = []
if function_calls:
    for call in function_calls:
        call_results.append(call_function(call, verbose))
    if len(call_results) > 1:
        print("more than one")
    try:
        a = f"-> {call_results[0].parts[0].function_response.response}"
        if verbose:
            print(a)
    except Exception as e:
        raise Exception("Error:", e)
    if not call_results:
        raise Exception("no function responses generated, exiting.")

else:
    print("Text:", resp.text)


if resp.usage_metadata is not None and verbose:
    print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
    print("Response tokens:", resp.usage_metadata.candidates_token_count)
elif verbose:
    print("Couldn't get usage metadata")


