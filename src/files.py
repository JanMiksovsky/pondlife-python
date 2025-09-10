from pathlib import Path

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
