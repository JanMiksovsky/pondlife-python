import markdown

from .files import readFiles
from .parse_date import parse_date
from .utils import document_dict

# Read markdown posts
post_files = readFiles("markdown")
post_md_docs = {key: {**document_dict(file), "date": parse_date(key)} for key, file in post_files.items()}
post_html_docs = {
    key.removesuffix(".md") + ".html": {**mdDoc, "_body": markdown.markdown(mdDoc["_body"])}
    for key, mdDoc in post_md_docs.items()
}

post_docs = dict(reversed(list(post_html_docs.items())))
