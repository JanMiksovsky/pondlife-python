from pathlib import Path
import os

def readFiles(folder: str) -> dict[str, str]:
    """
    Read all files in a folder (non-recursively) and return a dict
    mapping filename -> file contents (as text).
    """
    folder_path = Path(folder)
    result = {}
    for file in folder_path.iterdir():
        if file.is_file():
            result[file.name] = file.read_text()
    return result

def writeFiles(folder, files_dict):
    """Write each (key, value) in files_dict to a file named key in folder, with value as content."""
    os.makedirs(folder, exist_ok=True)
    for filename, content in files_dict.items():
        file_path = os.path.join(folder, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
