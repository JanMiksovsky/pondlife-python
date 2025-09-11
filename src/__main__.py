from .files import clearFiles, writeFiles
from .site_tree import site_tree

clearFiles("build")
writeFiles("build", site_tree)
