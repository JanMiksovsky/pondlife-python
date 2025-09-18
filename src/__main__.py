from .folder import Folder
from .site_tree import site_tree

build = Folder("build")
build.clear()
build.update(site_tree)
