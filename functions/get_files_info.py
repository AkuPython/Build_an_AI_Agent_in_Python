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

