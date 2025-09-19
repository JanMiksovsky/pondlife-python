"""
Command-line interface for building and serving the site
"""


import sys
from typing import Mapping

from .blog_site import blog_site
from .folder import Folder
from .serve import serve


def build(mapping: Mapping):
    """Given a mapping representing the site structure, build the site."""
    build_folder = Folder("build")
    build_folder.clear()
    build_folder.update(mapping)


def main():
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
        if cmd == "build":
            build(blog_site)
            return
        if cmd == "serve":
            serve(blog_site)
    print("usage: python -m src [build|serve]")
    sys.exit(1)


if __name__ == "__main__":
    main()
