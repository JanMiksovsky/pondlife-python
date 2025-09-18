import json
from pathlib import Path

from .folder import Folder
from .json_feed import json_feed
from .json_feed_to_rss import json_feed_to_rss
from .post_docs import post_docs
from .templates.multi_post_page import multi_post_page
from .templates.page import page
from .templates.single_post_page import single_post_page
from .utils import invoke_fns, md_doc_to_html_doc, paginate, text_to_doc

here = Path(__file__).parent


def about_html():
    """About page"""
    # About page
    about_path = here / "about.md"
    about_md = about_path.read_text(encoding="utf-8")
    about_md_doc = text_to_doc(about_md)
    about_html_doc = md_doc_to_html_doc(about_md_doc)
    return page(about_html_doc)


def feed():
    return json_feed(post_docs)


def pages_area():
    paginated = paginate(post_docs)
    return {
        f"{i + 1}.html": multi_post_page(page)
        for i, page in enumerate(paginated)
    }


def posts_area():
    return {
        key: single_post_page(document, key, post_docs)
        for key, document in post_docs.items()
    }


site_tree = invoke_fns({
    "about.html": lambda : about_html(),
    "assets": lambda: Folder(here / "assets"),
    "feed.json": lambda: json.dumps(feed(), indent=2),
    "feed.xml": lambda: json_feed_to_rss(feed()),
    "images": lambda: Folder(here / ".." / "images"),
    "index.html": lambda: pages_area()["1.html"], # same as pages/1.html
    "pages": lambda: pages_area(),
    "posts": lambda: posts_area(),
    "test.txt": lambda : "This is a test file.",
})
