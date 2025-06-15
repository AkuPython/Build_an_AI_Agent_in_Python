import os
from google.genai import types

def write_file(working_directory, file_path, content):
    root = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(root):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    file_dir = os.path.dirname(abs_file_path)
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    except Exception as e:
        return f'Error: Issue creating dirs: "{file_path}", {e}'
    try:
        with open(abs_file_path, "w") as f:
            size = f.write(content)
        return f'Successfully wrote to "{file_path}" ({size} characters written)'
    except Exception as e:
        return f'Error: Issue writing file: "{file_path}", {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in the specified directory (overwrite if it exists), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to write a file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The file contents to write to the file_path.",
            ),
        },
        required=["file_path", "content"],
    )
)
