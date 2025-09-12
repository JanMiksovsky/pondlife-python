import markdown

from .files import readFiles
from .parse_date import parse_date
from .utils import add_next_previous, document_dict

# Read markdown posts
post_files = readFiles("markdown")
post_md_docs = {key: {**document_dict(file), "date": parse_date(key)} for key, file in post_files.items()}
post_html_docs = {
    key.removesuffix(".md") + ".html": {**mdDoc, "_body": markdown.markdown(mdDoc["_body"])}
    for key, mdDoc in post_md_docs.items()
}

# Add `next_key`/`previous_key` properties so the post pages can be linked. The
# posts are already in chronological order because their names start with a
# YYYY-MM-DD date, so we can determine the next and previous posts by looking at
# the adjacent posts in the list. We need to do this before reversing the order
# in the next step; we want "next" to mean the next post in chronological order,
# not display order.
cross_linked = add_next_previous(post_html_docs)

# Entries are sorted by date; reverse for latest first
post_docs = dict(reversed(list(cross_linked.items())))