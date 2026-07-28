import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the Python script at file_path and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional command-line arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}: {result.stderr.strip()}"
        if result.stdout is None and result.stderr is None:
            return "No output produced"
        stdout_output = f"STDOUT: {result.stdout}"
        stderr_output = f"STDERR: {result.stderr}"
        return f"{stdout_output}\n{stderr_output}"
    except Exception as e:
        return f"Error: {e}"