import sys
from typing import Mapping

from .folder import Folder
from .serve import serve
from .site_tree import site_tree


def build(mapping: Mapping):
    """Given a mapping representing the site structure, build the site."""
    build_folder = Folder("build")
    build_folder.clear()
    build_folder.update(mapping)

def main():
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
        if cmd == "build":
            build(site_tree)
            return
        elif cmd == "serve":
            serve(site_tree)

    print("usage: python -m src [build|serve]")
    sys.exit(1)

if __name__ == "__main__":
    main()
