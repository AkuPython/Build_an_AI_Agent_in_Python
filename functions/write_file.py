import os
# from config import MAX_CHARS

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

