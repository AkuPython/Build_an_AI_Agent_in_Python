import os

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
    if not os.path.isfile(file_content_string):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000
    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
    return file_content_string
