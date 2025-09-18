import sys

from .folder import Folder
from .site_tree import site_tree


def build():
    build_folder = Folder("build")
    build_folder.clear()
    build_folder.update(site_tree)

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src [build|serve]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "build":
        build()
    # elif cmd == "serve":
    #     serve()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
