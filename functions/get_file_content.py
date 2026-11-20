import os

MAX_CHARS = 10_000

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get file content in a specified directory relative to the working directory, providing file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
  working_dir = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir, file_path))
  valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir
  
  if not(valid_target_dir):
    return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
  
  if os.path.isdir(target_dir):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  result = { "truncated": False}
  try:
    with open(target_dir, "r") as f:
      file_content_string = f.read(MAX_CHARS)
      result["content"] = file_content_string
      result["length"] = len(file_content_string)
      # print(f"file_content_string: {file_content_string}")
      if f.read(1):
        # content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        result["truncated"] = True
  except:
    return f"Error: {target_dir}"
    
  print_result = ""
  if result["truncated"]:
    print_result = f"{file_path} length: {len(file_content_string)}\n{file_path} truncated: {'truncated' in result}"
    # print_result = f"{file_path} truncated: {'truncated' in result}"
  else:
    print_result = result["content"]
  return print_result