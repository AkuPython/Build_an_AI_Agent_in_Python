import os
from config import MAX_CHARS

def get_files_info(working_directory, directory=None):
    if not isinstance(directory, str) or directory == None:
        f'Error: directory must be a string'
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

def get_file_content(working_directory, file_path):
    root = os.path.abspath(working_directory)
    file_content_string = root
    if file_path:
        file_content_string = os.path.abspath(os.path.join(working_directory, file_path))
    if not root in file_content_string:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.isfile(file_content_string):
            return f'Error: File not found or is not a regular file: "{file_content_string}"'
        with open(file_content_string, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f'Error: File not found or is not a regular file: "{file_path}", {e}'
