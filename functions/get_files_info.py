import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if not isinstance(directory, str) or directory == None:
        directory = ""
    assert isinstance(directory, str)
    root = os.path.abspath(working_directory)
    branch = root
    if directory:
        branch = os.path.abspath(os.path.join(working_directory, directory))
    if not root in branch:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(branch):
        return f'Error: "{directory}" is not a directory'
    try:
        files = []
        for f in os.listdir(branch):
            wf = os.path.abspath(os.path.join(branch, f))
            d = os.path.isdir(wf)
            s = os.path.getsize(wf)
            files.append(f'- {f}: file_size={s} bytes, is_dir={d}')
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
