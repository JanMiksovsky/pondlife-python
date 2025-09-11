from .files import clearFiles, writeFiles
from .tree import siteTree

clearFiles("build")
writeFiles("build", siteTree)
