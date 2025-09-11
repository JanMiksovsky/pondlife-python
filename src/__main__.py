from .files import clearFiles, writeFiles
from .siteTree import siteTree

clearFiles("build")
writeFiles("build", siteTree)
