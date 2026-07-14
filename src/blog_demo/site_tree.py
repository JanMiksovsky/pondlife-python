"""
Defines the site tree: a nested hierarchy of the site's resources.
"""


import json
from pathlib import Path

from map_origami import (FolderMap, document, invoke_fns, map_extensions,
                         map_items, paginate)

from .json_feed import json_feed
from .json_feed_to_rss import json_feed_to_rss
from .md_doc_to_html import md_doc_to_html
from .post_docs import post_docs
from .templates import templates

here = Path(__file__).parent


def about_html():
    """About page"""
    path = here / "about.md"
    md_text = path.read_text(encoding="utf-8")
    md_doc = document(md_text)
    html_doc = md_doc_to_html(md_doc)
    return templates["page"](value=html_doc, key=None, map=None)


def pages_area():
    """
    Paginated set of posts: 1.html, 2.html, etc.
    Each set contains 10 posts.
    """
    paginated = paginate(post_docs)
    return map_extensions(paginated, "->.html", value=templates["multi_post_page"])


def posts_area():
    """Individual post pages: 2025-07-04.html, etc."""
    return map_items(post_docs, value=templates["single_post_page"])


feed = json_feed(post_docs)

# The site tree is a tree with Mappings for interior nodes and the desired
# resources as leaves. Areas which are just Mappings are inherently lazy and are
# defined directly.
site_tree = {
    "about.html": about_html(),
    "assets": FolderMap(here / "assets"),
    "feed.json": json.dumps(feed, indent=2),
    "feed.xml": json_feed_to_rss(feed),
    "images": FolderMap(here / ".." / ".." / "images"),
    "index.html": pages_area()["1.html"],  # same as pages/1.html
    "pages": pages_area(),
    "posts": posts_area(),
}
