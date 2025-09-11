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

import markdown

from .files import readFiles
from .templates.postFragment import postFragment
from .utils import documentDict

postFiles = readFiles("markdown")
postMdDocs = {key: documentDict(file) for key, file in postFiles.items()}
postHtmlDocs = {
    key.removesuffix(".md") + ".html": {**mdDoc, "_body": markdown.markdown(mdDoc["_body"])}
    for key, mdDoc in postMdDocs.items()
}
postFragments = {
    key: postFragment(document, key)
    for key, document in postHtmlDocs.items()
}

siteTree = postFragments
