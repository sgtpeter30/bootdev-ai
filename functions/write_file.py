import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write to file content in a specified directory relative to the working directory, providing file path, and content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content you want to write to file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
  working_dir = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir, file_path))
  valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir
  
  if not(valid_target_dir):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  if os.path.isdir(target_dir):
    return f'Error: Cannot write to "{file_path}" as it is a directory'
  
  if not(os.path.isdir(working_dir)):
    os.makedirs(target_dir, exist_ok=True)
  
  try:  
    with open(target_dir, "w") as f:
      f.write(content)
      return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'      
  except NameError:
    # return f"Error: {NameError} {target_dir}"
    return f"Error: {target_dir}"