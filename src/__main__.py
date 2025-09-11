from .files import writeFiles
from .tree import siteTree

writeFiles("build", siteTree)
