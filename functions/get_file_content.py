import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    root = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(root):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS + 1)
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: Issue reading file: "{file_path}", {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns up to {MAX_CHARS} characters of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to get the content of, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
