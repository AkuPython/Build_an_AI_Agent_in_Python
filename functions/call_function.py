from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

fun_calls = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

root = "./calculator"

def call_function(function_call_part, verbose=False):
    print_str = f" -Calling function: {function_call_part.name}"
    fun_name = function_call_part.name
    if verbose:        
        print_str += f"({function_call_part.args})"
    print(print_str)
    if (fun := fun_calls.get(fun_name)) == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fun_name,
                    response={"error": f"Unknown function: {fun_name}"},
                )
            ],
        )

    function_call_part.args.update({"working_directory": root})
    fun_res = fun(**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fun_name,
                response={"result": fun_res},
            )
        ],
    )
