"""
Markdown post pipeline

This reads a folder of markdown posts, converts them to document objects (front
matter + HTML body), adds next/previous links, and sorts them most recent first.
"""


from .folder import Folder
from .parse_date import parse_date
from .utils import (add_next_previous, map_items, md_doc_to_html_doc,
                    text_to_doc)

# Read markdown posts as document objects
post_folder = Folder("markdown")
post_md_docs = map_items(post_folder, value=text_to_doc)

# Add a date property parsed from the filename
with_date = map_items(
    post_md_docs,
    value=lambda doc, key: {**doc, "date": parse_date(key)}
)

# Convert the document body to HTML
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

# Entries are sorted by date (because file name starts with date, and `Folder`
# uses natural sort order); reverse the order for latest first
post_docs = dict(reversed(list(cross_linked.items())))
