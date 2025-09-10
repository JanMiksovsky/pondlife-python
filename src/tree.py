# siteTree = {
#     "post1.md": {
#         "title": "My first post",
#         "date": "2026-07-04",
#         "body": "<p>This is the body of my first post.</p>"
#     },
#     "post2.md": {
#         "title": "Another post",
#         "date": "2026-07-05",
#         "body": "<p>This is the body of another post.</p>"
#     }
# }

from .templates.postFragment import postFragment
from .utils import documentDict
from .files import readFiles

postFiles = readFiles("markdown")
postDocuments = {key: documentDict(value) for key, value in postFiles.items()}
postPages = {key: postFragment(value, key) for key, value in postDocuments.items()}

siteTree = postDocuments
