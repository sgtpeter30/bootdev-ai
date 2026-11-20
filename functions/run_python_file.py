import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run Python file in a specified directory relative to the working directory, providing file path, and if needed additional args",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments for the script",
                },
                "required": ["file_path"],
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
  working_dir = os.path.abspath(working_directory)
  target_file = os.path.normpath(os.path.join(working_dir, file_path))
  valid_target_dir = os.path.commonpath([working_dir, target_file]) == working_dir
  
  if not(valid_target_dir):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(target_file):
    return f'Error: "{file_path}" does not exist or is not a regular file'
  
  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file'
  
  command = ["python", target_file]
  try:
    if args:
      command.extend(args)
    
    complete_process = subprocess.run(
      command,
      cwd=working_dir, 
      capture_output=True,
      text=True, 
      timeout=30
      )
  except subprocess.TimeoutExpired:
      return "Error: execution timed out after 30 seconds"
  except Exception as e:
      return f"Error: executing Python file: {e}"
    
  output_str = ""
  if complete_process.returncode != 0:  
    output_str += f"Process exited with code {complete_process.returncode}"
  if complete_process.stdout == None and complete_process.stderr == None:
    output_str += f"No output produced"
  else:
    output_str += f"STDOUT: {complete_process.stdout}"
    output_str += f"STDERR: {complete_process.stderr}"
  
  return output_str
    