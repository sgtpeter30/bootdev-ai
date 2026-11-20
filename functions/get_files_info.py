import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
  returnList = []
  
  working_dir = os.path.abspath(working_directory)
  target_dir = os.path.normpath(os.path.join(working_dir, directory))
  # Will be True or False
  valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir
  
  if not(valid_target_dir):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

  if not os.path.isdir(target_dir):
    return f'Error: "{directory}" is not a directory'
  
  if directory == '.':
    returnList.append(f"Result for current directory:")
  else:
    returnList.append(f"Result for '{directory}' directory:")
    
  item_list = os.listdir(target_dir)
  
  for item in item_list:
    fullPath = os.path.join(target_dir, item)
    is_dir = os.path.isdir(fullPath)
    item_size = os.path.getsize(fullPath)
    
    try:
      returnList.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir}")
    except NameError:
      print("Error: {err}")

  # return f'Success: "{directory}" is within the working directory'
  
  return "\n".join(returnList)