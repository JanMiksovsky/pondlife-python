import os
from collections.abc import Mapping, MutableMapping
from pathlib import Path

import natsort


class Folder(MutableMapping):
    """
    File system folder as a lazy mutable mapping. Keys are file/subfolder names.
    Values are bytes (for files) or Folders (for subfolders).
    """

    def __init__(self, folder):
        p = folder if isinstance(folder, Path) else Path(folder)
        self.path = p.expanduser().resolve()

    def clear(self):
        """
        Delete everything in the folder (but not the folder itself). We'd prefer
        to use the base implementation of MutableMapping.clear(), but it calls
        __getitem__ on each item before deleting it. That's a waste; we can just
        delete things.
        """
        if self.path.exists() and self.path.is_dir():
            for entry in self.path.iterdir():
                if entry.is_file():
                    entry.unlink()  # Delete the file
                elif entry.is_dir():
                    Folder(entry).clear()  # Recursively clear subfolder
                    entry.rmdir()  # Remove cleared subfolder

    def __delitem__(self, key):
        """Delete a file or subfolder."""
        os.makedirs(self.path, exist_ok=True)
        entry_path = self.path / key
        if entry_path.is_file():
            entry_path.unlink()
        elif entry_path.is_dir():
            Folder(entry_path).clear()
            entry_path.rmdir()
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        """Get the contents of a file, or a Folder for a subfolder."""
        entry_path = self.path / key
        if entry_path.is_file():
            return entry_path.read_bytes()
        if entry_path.is_dir():
            return Folder(entry_path)
        raise KeyError(key)

    def __iter__(self):
        if not self.path.exists():
            return
        yield from (entry.name for entry in natsort.natsorted(self.path.iterdir()))

    def __len__(self):
        if not self.path.exists():
            return 0
        return sum(1 for _ in self.path.iterdir())

    def __setitem__(self, key, value):
        """Write a subfolder for a dict, or the contents of a file."""
        os.makedirs(self.path, exist_ok=True)
        entry_path = self.path / key
        if isinstance(value, Mapping):
            # Recursively write subfolder
            Folder(entry_path).update(value)
        else:
            data = value if isinstance(value, bytes) else value.encode("utf-8")
            with open(entry_path, "wb") as f:
                f.write(data)
