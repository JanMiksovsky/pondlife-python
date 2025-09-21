"""
Command-line interface for building and serving the site
"""


import sys
from datetime import datetime
from typing import Mapping

from map_origami import Folder, serve

from .site_tree import site_tree


def build(m: Mapping):
    """
    Given a mapping representing the site structure, copy the entire tree into
    the build folder to create static files.
    """
    build_folder = Folder("build")
    build_folder.clear()
    build_folder.update(m)


def main():
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
        if cmd == "build":
            build(site_tree)
            return
        if cmd == "serve":
            serve(site_tree)
    print("usage: demo [build|serve]")
    sys.exit(1)


if __name__ == "__main__":
    main()
