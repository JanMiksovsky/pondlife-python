from pathlib import Path

import markdown

from .files import readFiles
from .templates.multiPostPage import multiPostPage
from .templates.page import page
from .templates.singlePostPage import singlePostPage
from .utils import documentDict, mdDocToHtmlDoc

# Read markdown posts
postFiles = readFiles("markdown")
postMdDocs = {key: documentDict(file) for key, file in postFiles.items()}
postHtmlDocs = {
    key.removesuffix(".md") + ".html": {**mdDoc, "_body": markdown.markdown(mdDoc["_body"])}
    for key, mdDoc in postMdDocs.items()
}

# About page
here = Path(__file__).parent
aboutPath = here / "about.md"
aboutMd = aboutPath.read_text(encoding="utf-8")
aboutMdDoc = documentDict(aboutMd)
aboutHtmlDoc = mdDocToHtmlDoc(aboutMdDoc)

# Assets
assets = readFiles(here / "assets")

# Static images
images = readFiles("images")

# Index page
indexPage = multiPostPage(postHtmlDocs)

# Posts area
postPages = {
    key: singlePostPage(document, key)
    for key, document in postHtmlDocs.items()
}

siteTree = {
    "about.html": page(aboutHtmlDoc),
    "assets": assets,
    "images": images,
    "index.html": indexPage,
    "posts": postPages,
}
