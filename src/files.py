from pathlib import Path
import os

def clearFiles(folder):
    """Delete all files and subfolders in the specified folder."""
    folder_path = folder if isinstance(folder, Path) else Path(folder)
    if folder_path.exists() and folder_path.is_dir():
        for entry in folder_path.iterdir():
            if entry.is_file():
                entry.unlink()  # Delete the file
            elif entry.is_dir():
                clearFiles(entry)  # Recursively clear subfolder
                entry.rmdir()  # Remove the empty subfolder

def readFiles(folder) -> dict:
    """
    Read all files in a folder (recursively) and return a dict
    mapping filename -> file contents (as text),
    and subfolder name -> sub-dictionary.
    Accepts either a str or Path object for folder.
    """
    folder_path = folder if isinstance(folder, Path) else Path(folder)
    result = {}
    for entry in folder_path.iterdir():
        if entry.is_file():
            result[entry.name] = entry.read_text()
        elif entry.is_dir():
            # Recursively read subfolder using Path object
            result[entry.name] = readFiles(entry)
    return result

def writeFiles(folder, files_dict):
    """Write each (key, value) in files_dict to a file named key in folder, with value as content."""
    os.makedirs(folder, exist_ok=True)
    for name, content in files_dict.items():
        path = os.path.join(folder, name)
        if isinstance(content, dict):
            # Recursively write subfolder
            writeFiles(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
