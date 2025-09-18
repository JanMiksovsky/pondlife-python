"""Markdown post pipeline"""

from .folder import Folder
from .parse_date import parse_date
from .utils import (add_next_previous, map_items, md_doc_to_html_doc,
                    text_to_doc)

# Read markdown posts
post_folder = Folder("markdown")
post_md_docs = map_items(post_folder, value=text_to_doc)
with_date = map_items(
    post_md_docs,
    value=lambda doc, key: {**doc, "date": parse_date(key)}
)
post_html_docs = map_items(
    with_date,
    key=lambda k: k.removesuffix(".md") + ".html",
    inverse_key=lambda k: k.removesuffix(".html") + ".md",
    value=md_doc_to_html_doc
)

# Add `next_key`/`previous_key` properties so the post pages can be linked. The
# posts are already in chronological order because their names start with a
# YYYY-MM-DD date, so we can determine the next and previous posts by looking at
# the adjacent posts in the list. We need to do this before reversing the order
# in the next step; we want "next" to mean the next post in chronological order,
# not display order.
cross_linked = add_next_previous(dict(post_html_docs))

# Entries are sorted by date; reverse for latest first
post_docs = dict(reversed(list(cross_linked.items())))
