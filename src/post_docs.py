"""
Markdown post pipeline

This reads a folder of markdown posts, converts them to document objects (front
matter as properties, plus a `_body` property), adds next/previous links, and
sorts them most recent first.

Each step represents the posts as a Mapping, chaning the values (and sometimes
the keys) as need.

The final value, `post_docs`, is a Mapping of HTML posts, keyed by the desired
file name (slug + ".html"), with properties:

- title
- date (a datetime)
- _body (HTML)
- next_key (the key of the next post, or None)
- previous_key (the key of the previous post, or None)
"""


from .folder import Folder
from .parse_date import parse_date
from .utils import (add_next_previous, map_items, md_doc_to_html_doc,
                    text_to_doc)

# Read markdown posts as text
post_folder = Folder("markdown")

# Convert text to document objects
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
cross_linked = add_next_previous(post_html_docs)

# Entries are sorted by date (because file name starts with date, and `Folder`
# uses natural sort order); reverse the order for latest first
post_docs = dict(reversed(list(cross_linked.items())))
