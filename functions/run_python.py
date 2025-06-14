import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    root = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(root):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    output = []
    try:
        args = [] if args == None else args
        out = subprocess.run(
            ["python", abs_file_path] + args,
            cwd=root,
            capture_output=True,
            timeout=30,
            text=True
        )
        output.append("STDOUT: " + out.stdout)
        output.append("STDERR: " + out.stderr)
        if not out.stdout and not out.stderr:
            output.append("No output produced")
        if not out.returncode == 0:
            output.append(f"Process exited with code {out.returncode}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

